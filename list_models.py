from google import genai
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)
models = client.models.list()
print("Available models:")
for m in models:
    if "generateContent" in m.supported_generation_methods:
        print(f"- {m.name}")
