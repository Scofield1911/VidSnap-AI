
import requests
import os

def generate_images(prompts, folder):
    """
    Generates images from prompts using Pollinations.ai (Free)
    """
    output_folder = f"user_uploads/{folder}"
    os.makedirs(output_folder, exist_ok=True)
    
    generated_files = []
    
    print(f"Generating {len(prompts)} images for {folder}...")
    
    for i, prompt in enumerate(prompts):
        try:
            # Pollinations.ai API
            # Encode prompt
            safe_prompt = requests.utils.quote(prompt)
            
            # Try Model 1: Flux (High Quality)
            url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1080&height=1920&seed={i}&model=flux"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            
            print(f"Requesting image {i} (Flux)...")
            response = requests.get(url, headers=headers, timeout=30)
            
            success = False
            if response.status_code == 200 and "image" in response.headers.get("Content-Type", ""):
                 success = True
            else:
                 print(f"Flux failed (Status: {response.status_code}, Type: {response.headers.get('Content-Type')}). Retrying with Turbo...")
                 # Try Model 2: Turbo (Faster, potentially more reliable)
                 url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1080&height=1920&seed={i}&model=turbo"
                 response = requests.get(url, headers=headers, timeout=20)
                 if response.status_code == 200 and "image" in response.headers.get("Content-Type", ""):
                     success = True
            
            if success:
                filename = f"image_{i}.jpg"
                filepath = os.path.join(output_folder, filename)
                
                with open(filepath, "wb") as f:
                    f.write(response.content)
                
                generated_files.append(filename)
                print(f"Generated: {filename}")
            else:
                print(f"Failed to generate image {i}")
                
        except Exception as e:
            print(f"Error generating image {i}: {e}")
            
    return generated_files

if __name__ == "__main__":
    # Test
    test_prompts = ["A futuristic cyberpunk city with neon lights", "A serene mountain landscape at sunset"]
    os.makedirs("user_uploads/test_gen", exist_ok=True)
    generate_images(test_prompts, "test_gen")
