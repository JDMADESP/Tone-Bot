
from dotenv import load_dotenv
import sys
import argparse
import os
from openai import OpenAI



def relay_message(message: str | None, tone: str | None) -> (str):
  #Uses input of message and tone to output the modified
  #new message with a modified new tone
  load_dotenv('.env')
  key = os.getenv('API_KEY')
  # ast = os.getenv('AST_KEY')
  client = OpenAI(api_key=key)
  completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are an editor who is in charge of" +
                                   "changing the tones of phrases to the" +
                                   "specified new tone."},
    {"role": "user", "content": ("Using a " + tone + "tone change the sentence"
                                 "Change:" + message)}
  ]
)
  return completion.choices[0].message.content

def check_if_tone(tone_test):
  #Checks if the second argument passed into the command line
  #is actually a word or phrase that describes a tone
  load_dotenv('.env')
  key = os.getenv('API_KEY')
  client = OpenAI(api_key=key)
  completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": ("You are an editor who is in charge of" + 
                                   "deciding if a bunch of input words or a word" + 
                                   "describe a type of tone." + "A few examples of" +
                                   "tones would be a happy, casual, sad, formal."
                                   "If the words describe a tone, just respond with: yes")},
    {"role": "user", "content": tone_test}
  ]
)
  tone_return = completion.choices[0].message.content
  print(tone_return)
  if tone_return == "Yes":
    return True
  else:
    return False
  

def main():
  if len(sys.argv) != 3:
    print("Not Enough arguments or too many arguments")
    return
  parser = argparse.ArgumentParser(description='Tone Editor')
  parser.add_argument('message', type=str, help='Sentence')
  parser.add_argument('tone', type=str,help='Tone')
  args = parser.parse_args()
  tone_check = check_if_tone(args.tone)
  print(tone_check)
  if tone_check: #if second argument is a tone
    message_sending = args.message
    tone_sending = args.tone
  else:
    print("Your second argument is not a tone")
    return
  response = relay_message(message_sending, tone_sending)
  print(response)        


if __name__ == '__main__':
  main()


# completion = client.chat.completions.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "system", "content": "You are an editor who is in charge of changing the tones of phrases to the specified new tone."},
#     {"role": "user", "content": "Change the paragraph to a happy tone. The paragraph is as follows: In the dim light of the fading evening, an old man sat silently on the worn park bench, his eyes tracing the path of a solitary leaf drifting to the ground. Each wrinkle on his face seemed to tell a story of a cherished memory now lost to time. As the chill of the night set in, he pulled his coat tighter, the empty space beside him feeling colder than the autumn air."}
#   ]
# )

# print(completion.choices[0].message.content)