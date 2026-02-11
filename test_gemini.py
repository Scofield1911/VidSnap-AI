from google import genai
from config import GEMINI_API_KEY
import sys

try:
    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(
        model='gemini-2.0-flash-exp',
        contents='Explain how AI works in one sentence.'
    )
    print("Success with gemini-2.0-flash-exp:")
    print(response.text)
except Exception as e:
    print(f"Failed with gemini-2.0-flash-exp: {e}")
    try:
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents='Explain how AI works in one sentence.'
        )
        print("Success with gemini-1.5-flash:")
        print(response.text)
    except Exception as e2:
        print(f"Failed with gemini-1.5-flash: {e2}")
