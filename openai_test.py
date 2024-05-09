
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv('.env')
key = os.getenv('API_KEY')
client = OpenAI(api_key=key)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are an editor who is in charge of changing the tones of sentences to the specified new tone."},
    {"role": "user", "content": "Change the sentence to a happy tone. The sentence is, Sadly, my mother just passed away"}
  ]
)

print(completion.choices[0].message.content)