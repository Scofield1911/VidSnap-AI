import requests
import os
from config import HF_TOKEN

API_URL = "https://api-inference.huggingface.co/models/facebook/musicgen-small"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def generate_music(prompt, output_folder, file_name="background_music.mp3"):
    """
    Generates music using Hugging Face's MusicGen model.
    """
    try:
        payload = {"inputs": prompt}
        response = requests.post(API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            os.makedirs(output_folder, exist_ok=True)
            file_path = os.path.join(output_folder, file_name)
            
            with open(file_path, "wb") as f:
                f.write(response.content)
                
            print(f"Music saved: {file_path}")
            return file_path
        else:
            print(f"Failed to generate music. Status code: {response.status_code}")
            print(response.json())
            return None
            
    except Exception as e:
        print(f"Error generating music: {e}")
        return None

if __name__ == "__main__":
    generate_music("lofi hip hop beat, chill, relaxing", "test_music")
