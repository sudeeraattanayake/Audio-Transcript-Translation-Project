from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY was not found")

client = OpenAI(api_key=api_key)

with open("test.ogg", "rb") as audio_file:
    output = client.audio.translations.create(
        model="whisper-1",
        file=audio_file
    )

print(output.text)
