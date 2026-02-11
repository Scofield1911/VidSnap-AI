from google import genai
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)
# Just print the first 5 models to verify names
for i, m in enumerate(client.models.list()):
    print(f"Model: {m.name}")
    if i >= 10: break
