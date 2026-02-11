
import asyncio
import edge_tts
import os

async def _generate_audio(text, output_file):
    voice = "en-US-ChristopherNeural"  # High quality male voice
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)

def text_to_speech_file(text, folder_id):
    """
    Generates speech from text using Microsoft Edge TTS (Free).
    """
    try:
        output_folder = f"user_uploads/{folder_id}"
        os.makedirs(output_folder, exist_ok=True)
        output_file = os.path.join(output_folder, "audio.mp3")
        
        # Run async function
        asyncio.run(_generate_audio(text, output_file))
        
        if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
            print(f"Generated audio: {output_file}")
            return output_file
        else:
            print("Failed to generate audio file.")
            return None
            
    except Exception as e:
        print(f"Error in TTS: {e}")
        return None

if __name__ == "__main__":
    # Test
    os.makedirs("user_uploads/test_tts", exist_ok=True)
    text_to_speech_file("Hello, this is a test of the free text to speech system.", "test_tts")
