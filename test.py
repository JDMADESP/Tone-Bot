
from dotenv import load_dotenv
import os

load_dotenv('.env')
key = os.getenv('API_KEY')

print(key)
print("Hello World")