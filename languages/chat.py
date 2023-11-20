
import os
import json
import glob
import random
import pygame
import keyboard
import sounddevice as sd
import numpy as np

from openai import OpenAI
from scipy.io.wavfile import write


# Local imports
from speak import play_audio

# API Key
from constants import OPENAPI_KEY


# Persona
SPANISH_TEACHER = '''I want you to act as a spoken Spanish teacher and improver.
I will speak to you in Spanish and you will reply to me in Spanish to practice my spoken Spanish.
I want you to keep your reply neat, limiting the reply to 100 words.
I want you to strictly correct my grammar mistakes, typos, and factual errors.
I want you to ask me a question in your reply.
Now let's start practicing, you could ask me a question first.
Remember, I want you to strictly correct my grammar mistakes, typos, and factual errors.
'''

class ChatBot:
    def __init__(self, persona: str, conversation_path: str):
        # Open AI Setup
        self.client = OpenAI(api_key=OPENAPI_KEY)
        self.messages = [ {"role": "system", "content": persona }]
        self.conversation_name = 'conversation1'
        self.conversation_path = conversation_path
        self.len_messages = len(self.messages)
        
    
    def update_len_messages(self):
        self.len_messages = len(self.messages)
        
        
        
    def update_transcript(self, text: str, role: str):
        new_transcript_text = f'{role}: {text}\n\n'
        
        with open(f'{self.conversation_path}/transcript.txt', 'a+') as file:
            file.write(new_transcript_text)
            
    
    def generate_text(self):
        print('Messages', self.messages)
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            # model="gpt-4-1106-preview",
            messages=self.messages
        )
        response = response.choices[0].message.content
        print('Finished Generating Text...')
        print(response)
        
        return response
        
    
    def generate_audio(self, text: str, role: str):
        audio_file = f'{self.conversation_path}/{role}_{self.len_messages}.mp3'
        audio_response = self.client.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=text
        )
        
        audio_response.stream_to_file(audio_file)
        
        return audio_file
        

    def play_audio(self, audio_file: str):
        pygame.mixer.init()
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()

        # Wait for the audio to finish playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            
            
    def add_user_input(self, user_input: str):
        self.messages = self.messages + [{ "role": "user", "content": user_input }]
        self.update_len_messages()
        self.update_transcript(user_input, 'user')
        
      
    def generate_response(self, user_input: str):
        # Save User Input
        self.add_user_input(user_input)
        
        # Generate Chat Response
        response = self.generate_text()
        self.messages = self.messages + [{ "role": "system", "content": response }]
        
        # Update Transcript
        self.update_transcript(response, 'system')
        
        # Generate the Audio
        audio_file = self.generate_audio(response, 'system')
        
        # Play the Audio
        self.play_audio(audio_file)
        
    
    def start_chat(self):
        # Generate Initial Text
        initial_text = self.generate_text()
        
        # Initial Audio
        intial_audio = self.generate_audio(initial_text, 'system')
        
        # Play Initial Audio
        self.play_audio(intial_audio)
        
   
class VoiceRecorder:
    def __init__(self, conversation_path: str, sample_rate=44100, channels=2, duration=10):
        # Open AI Setup
        self.client = OpenAI(api_key=OPENAPI_KEY)
        self.conversation_path = conversation_path
        
        # Audio Setup
        self.sample_rate = sample_rate
        self.channels = channels
        self.duration = duration
        self.recording = False
        self.audio_data = []
        
        
    def save_to_wav(self, filename='recorded_audio.wav'):
        audio_data = np.concatenate(self.audio_data, axis=0)
        write(filename, self.sample_rate, audio_data)
        print(f"Recording saved as {filename}")


    def callback(self, indata, frames, time, status):
        if status:
            print(status, flush=True)
        self.audio_data.append(indata.copy())


    def start_recording(self):
        print("Press Enter to start recording...")
        keyboard.wait("enter")
        self.recording = True

        with sd.InputStream(callback=self.callback, channels=self.channels, samplerate=self.sample_rate):
            print('Recording')
            keyboard.wait("enter")
            self.recording = False

        random_number = random.randint(0,90000000000)
        filename = f'{self.conversation_path}/user_{random_number}.wav'
        self.save_to_wav(filename)
        
        # Transcribe Input
        audio_file= open(filename, "rb")
        transcript = self.client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file, 
            response_format="text"
        )
        
        return transcript



def setup_conversation():
    # Get the current working directory
    base_directory = os.getcwd()

    # Specify the name of the new folder
    conversation_folders = glob.glob('conversation*')
    # Filter out only the directories
    conversation_folders = [folder for folder in conversation_folders if os.path.isdir(folder)]
    
    conversation = len(conversation_folders) + 1
    
    folder_name = f'conversation_{conversation}'
    folder_path = os.path.join(base_directory, folder_name)

    # Create the new folder
    try:
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created successfully.")
    except OSError as e:
        print(f"Error creating folder: {e}")
        
        
    return folder_name, folder_path


    
def main():
    
    new_conversation, conversation_path = setup_conversation()
    print('New Conversation', new_conversation, 'Conversation Path', conversation_path)
    
    spanish_teacher = ChatBot(persona=SPANISH_TEACHER, conversation_path=conversation_path)
    
    spanish_teacher.start_chat() 
    while True:
        recorder = VoiceRecorder(conversation_path=conversation_path)
        user_input = recorder.start_recording()
        print('User:', user_input)
        
        if user_input.lower() == 'cancel':
            print("Finished")
            break
        
        spanish_teacher.generate_response(user_input)




if __name__ == "__main__":
    main()