from google import genai
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)
with open("models.txt", "w") as f:
    for m in client.models.list():
        f.write(f"{m.name}\n")
print("Wrote models to models.txt")
