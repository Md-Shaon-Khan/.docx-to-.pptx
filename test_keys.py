import os
import requests
import openai
from dotenv import load_dotenv  # <-- import this

# Load .env file
load_dotenv()

# Load keys from environment
openai_key = os.getenv("OPENAI_API_KEY")
unsplash_key = os.getenv("UNSPLASH_ACCESS_KEY")

if not openai_key:
    print("OpenAI API key not found in environment!")
else:
    openai.api_key = openai_key

if not unsplash_key:
    print("Unsplash Access Key not found in environment!")

# Test OpenAI
try:
    if openai_key:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10
        )
        print("OpenAI Key is working!")
except Exception as e:
    print("OpenAI Key Error:", e)

# Test Unsplash
try:
    if unsplash_key:
        url = f"https://api.unsplash.com/photos/random?client_id={unsplash_key}&query=test"
        r = requests.get(url)
        if r.status_code == 200:
            print("Unsplash Key is working!")
        else:
            print("Unsplash Key Error:", r.status_code, r.text)
except Exception as e:
    print("Unsplash Key Error:", e)
