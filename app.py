
from dotenv import load_dotenv
import os
from openai import OpenAI
from flask import Flask, render_template, request, jsonify, make_response
# import sys
# import argparse


#Load our API_KEY
load_dotenv('.env')
key = os.getenv('API_KEY')
client = OpenAI(api_key=key)
languages = ["English", "Spanish"]

#Flask code help from Youtube Kamryn Ohly
#configure our flask app
app = Flask(__name__)
app.json.sort_keys = False

#enable auto-reload
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/", methods=["GET", "POST"])
def index():
  if request.method == "POST":
    if request.is_json: ##Get JSON Terms
      data = request.get_json()
      if not data:
        return jsonify({"error":"Incorrect Data"})
      phrases = data["phrases"]
      tone = data["tone"]
      language = data["languages"]
      outPhrases, costs = handle_Synch(phrases, tone, language)
    else: ##Get form terms
      prompt = request.form.get("prompt")
      tone = request.form.get("tone")
      language = request.form.get("languages")
    print(language)
    ##Check if inputted valid
    if not prompt:
      return jsonify({"error":"Error with prompt provided"})
    if not language:
      return jsonify({"error":"Error with language provided"})
    if not tone or (check_if_tone(tone) == False):
      return jsonify({"error":"Error with tone provided"})
    #######
    ###Get new message and tokens used
    message, tokens_used = relay_message(prompt, tone, language)
    return jsonify({"phrase": prompt, "tone": tone, "modifiedPhrase": message, "tokensUsed":tokens_used})
  else:
    return render_template("index.html", languages = languages)

def handle_Synch(phrases, tone, language):
  if not prompt:
      return jsonify({"error":"Error with prompt provided"})
  if not language:
    return jsonify({"error":"Error with language provided"})
  if not tone or (check_if_tone(tone) == False):
    return jsonify({"error":"Error with tone provided"})
  
  

def check_if_tone(tone_test):
  #Checks if the second argument passed into the command line
  #is actually a word or phrase that describes a tone
  completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": ("You are an editor who is in charge of" + 
                                   "deciding if a bunch of input words or a word" + 
                                   "describe a type of tone." + "A few examples of" +
                                   "tones in english would be a happy, casual, sad, formal."
                                   + "A few examples of not being a tone are sentences,"
                                   + "what's up my guy, paragraphs, what's up my guy."
                                   "If the words describe a tone, just respond with: yes. If it's not a tone, respond with: no")},
    {"role": "user", "content": tone_test}
  ]
)
  tone_return = completion.choices[0].message.content
  print(tone_return)
  # print(tone_return)
  if (tone_return == "Yes") or (tone_return == "yes"):
    return True
  else:
    return False


def relay_message(message: str | None, tone: str | None, lang: str | None) -> (str):
  #Uses input of message and tone to output the modified
  #new message with a modified new tone
  if lang == "English":
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": """You are in charge of changing the tone
                                      of a sentence. Only output the new sentence in english"""},
      {"role": "user", "content": ("Tone:" + tone + ". " "Phrases to"
                                  "change:" + message)}
    ]
  )
  else:
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": """Tu eres el encargado de cambiar el tono
                                      de una frase. Solo genera 
                                      la nueva oración en español"""},
      {"role": "user", "content": ("Tono:" + tone + ". " "Frase a cambiar:" 
                                   + message)}
    ]
    )
  ret_message = completion.choices[0].message.content
  num_tokens = completion.usage.total_tokens
  print(ret_message)
  return ret_message, num_tokens



# def relay_message(message: str | None, tone: str | None) -> (str):
#   #Uses input of message and tone to output the modified
#   #new message with a modified new tone
#   load_dotenv('.env')
#   key = os.getenv('API_KEY')
#   # ast = os.getenv('AST_KEY')
#   client = OpenAI(api_key=key)
#   completion = client.chat.completions.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "system", "content": "You are an editor who is in charge of" +
#                                    "changing the tones of phrases to the" +
#                                    "specified new tone." + "If the tone" +
#                                    "is not a valid tone, you should return:"+
#                                    "'You did not enter a valid tone'."},
#     {"role": "user", "content": ("Tone:" + tone + ". " "Phrases to"
#                                  "change:" + message)}
#   ]
# )
#   return completion.choices[0].message.content

# def check_if_tone(tone_test):
#   #Checks if the second argument passed into the command line
#   #is actually a word or phrase that describes a tone
#   load_dotenv('.env')
#   key = os.getenv('API_KEY')
#   client = OpenAI(api_key=key)
#   completion = client.chat.completions.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "system", "content": ("You are an editor who is in charge of" + 
#                                    "deciding if a bunch of input words or a word" + 
#                                    "describe a type of tone." + "A few examples of" +
#                                    "tones would be a happy, casual, sad, formal."
#                                    "If the words describe a tone, just respond with: yes")},
#     {"role": "user", "content": tone_test}
#   ]
# )
#   tone_return = completion.choices[0].message.content
#   print(tone_return)
#   if tone_return == "Yes":
#     return True
#   else:
#     return False
  

# def main():
#   if len(sys.argv) != 3:
#     print("Not Enough arguments or too many arguments")
#     return
#   parser = argparse.ArgumentParser(description='Tone Editor')
#   parser.add_argument('message', type=str, help='Sentence')
#   parser.add_argument('tone', type=str,help='Tone')
#   args = parser.parse_args()
#   tone_check = check_if_tone(args.tone)
#   print(tone_check)
#   if tone_check: #if second argument is a tone
#     message_sending = args.message
#     tone_sending = args.tone
#   else:
#     print("Your second argument is not a tone")
#     return
#   response = relay_message(message_sending, tone_sending)
#   print(response)        


# if __name__ == '__main__':
#   main()


# completion = client.chat.completions.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "system", "content": "You are an editor who is in charge of changing the tones of phrases to the specified new tone."},
#     {"role": "user", "content": "Change the paragraph to a happy tone. The paragraph is as follows: In the dim light of the fading evening, an old man sat silently on the worn park bench, his eyes tracing the path of a solitary leaf drifting to the ground. Each wrinkle on his face seemed to tell a story of a cherished memory now lost to time. As the chill of the night set in, he pulled his coat tighter, the empty space beside him feeling colder than the autumn air."}
#   ]
# )

# print(completion.choices[0].message.content)