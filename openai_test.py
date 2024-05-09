
from dotenv import load_dotenv
import argparse
import os
from openai import OpenAI



def relay_message(message):
  load_dotenv('.env')
  key = os.getenv('API_KEY')
  # ast = os.getenv('AST_KEY')
  client = OpenAI(api_key=key)
  completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are an editor who is in charge of changing the tones of phrases to the specified new tone."},
    {"role": "user", "content": message}
  ]
)
  return completion.choices[0].message.content

def main():
  parser = argparse.ArgumentParser(description='Tone Editor')
  parser.add_argument('message', type=str, help='Sentence and Tone to Change')
  args = parser.parse_args()
  message_sending = args.message
  response = relay_message(message_sending)
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