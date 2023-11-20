import pygame
import time

def play_audio(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

# # Replace "your_file.mp3" with the path to your audio file
# audio_file_path = "content.mp3"

# play_audio(audio_file_path)
