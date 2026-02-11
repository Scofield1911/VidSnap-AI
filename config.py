import os
from dotenv import load_dotenv

load_dotenv()

# config.py
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "your_actual_api_key_here")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY").strip() if os.getenv("GEMINI_API_KEY") else None
HF_TOKEN = os.getenv("HF_TOKEN")