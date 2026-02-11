from moviepy.editor import ImageClip, AudioFileClip, CompositeAudioClip, concatenate_videoclips, vfx
import os
import random

def create_video(folder, image_files, audio_file, music_file=None, output_path=None):
    """
    Combines images and audio into a video.
    """
    try:
        # Load Main Audio (Voiceover)
        voiceover = AudioFileClip(audio_file)
        duration = voiceover.duration
        
        # Calculate duration per image
        num_images = len(image_files)
        slide_duration = duration / num_images
        
        clips = []
        for img_path in image_files:
            # Create a clip for each image
            clip = ImageClip(img_path).set_duration(slide_duration)
            
            # Resize for vertical video (1080x1920)
            # This is a simple resize, might need cropping to fill
            clip = clip.resize(height=1920)
            clip = clip.crop(x1=clip.w/2 - 1080/2, y1=0, width=1080, height=1920) 
            
            # Optional: Add simple zoom effect/pan? (Keeping it simple for now)
            
            clips.append(clip)
            
        final_video = concatenate_videoclips(clips, method="compose")
        final_video = final_video.set_audio(voiceover)
        
        # Add Background Music if available
        if music_file:
            bg_music = AudioFileClip(music_file)
            
            # Loop music if shorter, cut if longer
            if bg_music.duration < duration:
                bg_music = n_loops = int(duration / bg_music.duration) + 1
                bg_music = bg_music.loop(n=n_loops)
                
            bg_music = bg_music.subclip(0, duration)
            
            # Lower volume of music
            bg_music = bg_music.volumex(0.15) 
            
            # Mix audio
            final_audio = CompositeAudioClip([voiceover, bg_music])
            final_video = final_video.set_audio(final_audio)

        # Output Path
        if not output_path:
            output_path = f"static/reels/{folder}.mp4"
            
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Write file
        final_video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
        return output_path
        
    except Exception as e:
        print(f"Error creating video: {e}")
        return None

if __name__ == "__main__":
    # Test
    pass
