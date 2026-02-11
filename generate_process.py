# this file looks for new folders in user_uploads and converts them into reel if not already processed

import os
import time
import subprocess
import json
from text_to_audio_free import text_to_speech_file
from image_gen import generate_images

def text_to_audio(folder, text):
    print("TTA -", folder)
    print(text, folder)
    # Re-using existing function, ensuring it takes text and folder
    # If the original text_to_audio function reads from file, we might need to adjust or just pass the text
    # checking original implementation of text_to_speech_file: it takes (text, folder) -> perfect.
    return text_to_speech_file(text, folder)

def create_reel(folder):
    # Check if we have images and audio
    upload_path = f"user_uploads/{folder}"
    
    # 1. Verify Audio
    if not os.path.exists(f"{upload_path}/audio.mp3"):
        print(f"Error: audio.mp3 not found for {folder}")
        return

    # 2. Check for images
    images = [f for f in os.listdir(upload_path) if f.startswith("image_") and f.endswith(".jpg")]
    if not images:
        print(f"Error: No generated images found for {folder}")
        # Validating if manual upload images exist (from original code flow)
        if not os.path.exists(f"{upload_path}/input.txt"):
             print(f"Error: No images and no input.txt for {folder}")
             return
    
    # 3. Build input.txt if it doesn't exist (AI Flow)
    if not os.path.exists(f"{upload_path}/input.txt"):
        print("Building input.txt for AI images...")
        images.sort() # Ensure image_0, image_1 order
        with open(f"{upload_path}/input.txt", "w") as f:
            for img in images:
                # Use absolute paths for FFmpeg to avoid CWD issues
                abs_path = os.path.abspath(f"{upload_path}/{img}").replace("\\", "/")
                f.write(f"file '{abs_path}'\nduration 3\n")
            # Repeat last image to prevent cut-off
            if images:
                 abs_path = os.path.abspath(f"{upload_path}/{images[-1]}").replace("\\", "/")
                 f.write(f"file '{abs_path}'\n")

    # 4. Run FFmpeg
    # Use absolute paths for inputs too
    abs_input_txt = os.path.abspath(f"user_uploads/{folder}/input.txt").replace("\\", "/")
    abs_audio = os.path.abspath(f"user_uploads/{folder}/audio.mp3").replace("\\", "/")
    abs_output = os.path.abspath(f"static/reels/{folder}.mp4").replace("\\", "/")
    
    command = f'''ffmpeg -y -f concat -safe 0 -i "{abs_input_txt}" -i "{abs_audio}" -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" -c:v libx264 -c:a aac -strict -2 -shortest -r 30 -pix_fmt yuv420p "{abs_output}"'''
    
    print(f"Running FFmpeg for {folder}...")
    try:
        subprocess.run(command, shell=True, check=True)
        print("CR - Success", folder)
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg failed for {folder}: {e}")
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg failed for {folder}: {e}")

def process_ai_folder(folder):
    """
    Handles the AI generation part: Prompts -> Images -> Audio
    """
    upload_path = f"user_uploads/{folder}"
    
    # Check if we have prompts but no images yet
    if os.path.exists(f"{upload_path}/prompts.json") and not os.path.exists(f"{upload_path}/image_0.jpg"):
        print(f"Found prompts for {folder}, generating images...")
        with open(f"{upload_path}/prompts.json", "r") as f:
            prompts = json.load(f)
        
        generate_images(prompts, folder)
        
    # Check if we have desc.txt (script) but no audio yet
    if os.path.exists(f"{upload_path}/desc.txt") and not os.path.exists(f"{upload_path}/audio.mp3"):
        print(f"Found script for {folder}, generating audio...")
        with open(f"{upload_path}/desc.txt", "r") as f:
            script_text = f.read()
            
        text_to_audio(folder, script_text)

if __name__ == "__main__":
    print("Worker running... waiting for jobs.")
    while True:
        if not os.path.exists("done.txt"):
            with open("done.txt", "w") as f: f.write("")
            
        with open("done.txt", "r") as f:
            done_folders = [f.strip() for f in f.readlines()]

        # Get list of all folders in user_uploads
        folders = os.listdir("user_uploads")
        
        for folder in folders:
            # Check if likely a temp folder or system folder
            if not os.path.isdir(f"user_uploads/{folder}"): continue
            
            if folder not in done_folders:
                print(f"Processing {folder}...")
                
                # 1. AI Content Generation (if applicable)
                if os.path.exists(f"user_uploads/{folder}/prompts.json") or os.path.exists(f"user_uploads/{folder}/desc.txt"):
                    try:
                        process_ai_folder(folder)
                    except Exception as e:
                        print(f"AI Generation failed for {folder}: {e}")
                        continue # Skip to next folder or retry?
                
                # 2. Video Assembly (FFmpeg)
                # Check if ready for video (has audio and input.txt OR images)
                is_ready = os.path.exists(f"user_uploads/{folder}/audio.mp3")
                if is_ready:
                     create_reel(folder)   
                     with open("done.txt", "a") as f:
                        f.write(folder + "\n")
        
        time.sleep(3)
