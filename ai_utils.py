from google import genai
import json
from config import GEMINI_API_KEY

def generate_script_and_prompts(topic):
    """
    Generates a video script and image prompts for a given topic using Gemini.
    """
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        prompt = f"""
        You are a professional viral content creator. 
        Create a 30-45 second engaging video script about: "{topic}".
        
        The output MUST be a valid JSON object with the following structure:
        {{
            "script": "The full voiceover text here...",
            "image_prompts": [
                "Detailed AI image generation prompt for scene 1",
                "Detailed AI image generation prompt for scene 2",
                "Detailed AI image generation prompt for scene 3",
                "Detailed AI image generation prompt for scene 4",
                "Detailed AI image generation prompt for scene 5"
            ]
        }}
        
        Rules:
        1. The script should be catchy, fast-paced, and suitable for Instagram Reels/TikTok.
        2. Provide exactly 5 distinct image prompts that visually match the progression of the script.
        3. The image prompts should be highly descriptive (e.g., "Cinematic shot of a futuristic city, neon lights, 8k resolution").
        4. Do not include markdown formatting like ```json ... ```. Just return the raw JSON string.
        """

        response = client.models.generate_content(
            model='gemini-2.5-flash', 
            contents=prompt
        )
        
        text_response = response.text.strip()
        
        # Clean up any potential markdown code blocks if the model ignores the instruction
        if text_response.startswith("```json"):
            text_response = text_response[7:]
        if text_response.startswith("```"):
            text_response = text_response[3:]
        if text_response.endswith("```"):
            text_response = text_response[:-3]
            
        data = json.loads(text_response)
        return data
        
    except Exception as e:
        print(f"Error generating content: {e}")
        # Fallback to 1.5 flash if 2.0 is not available
        try:
            print("Retrying with gemini-1.5-flash...")
            response = client.models.generate_content(
                model='gemini-1.5-flash', 
                contents=prompt
            )
            text_response = response.text.strip()
            if text_response.startswith("```json"): text_response = text_response[7:]
            if text_response.startswith("```"): text_response = text_response[3:]
            if text_response.endswith("```"): text_response = text_response[:-3]
            return json.loads(text_response)
        except Exception as e2:
            print(f"Fallback failed: {e2}")
            return None

if __name__ == "__main__":
    # Test the function
    print(f"Using API Key: {GEMINI_API_KEY[:5]}...{GEMINI_API_KEY[-5:]}")
    result = generate_script_and_prompts("The History of Coffee")
    if result:
        print(json.dumps(result, indent=4))
    else:
        print("Failed to generate script.")
