import whisper
import pyttsx3
import sounddevice as sd
import numpy as np
from chatbot import chatbot_response  # Custom doctor chatbot logic

# Initialize Whisper ASR
asr_model = whisper.load_model("base")  # Or "small", "medium", "large"

# Initialize pyttsx3 TTS
engine = pyttsx3.init()

def record_audio(duration=5, samplerate=16000):
    print("Listening...")
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='float32')
    sd.wait() 
    return np.squeeze(audio_data)

def speech_to_text(audio_data):
    result = asr_model.transcribe(audio_data)
    return result['text']

def text_to_speech(text):
    engine.say(text)
    engine.runAndWait()

def main():
    print("Start conversation with the doctor chatbot (say 'Goodbye' to exit).")
    
    while True:
        audio_data = record_audio()
        user_text = speech_to_text(audio_data)
        print(f"You: {user_text}")
        
        if "goodbye" in user_text.lower():
            print("Doctor: Take care! Goodbye.")
            text_to_speech("Take care! Goodbye.")
            break
    
        doctor_response = chatbot_response(user_text)
        print(f"Doctor: {doctor_response}")
        
        text_to_speech(doctor_response)

if __name__ == "__main__":
    main()

