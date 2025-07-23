import os
import pyaudio
import wave
import json
from vosk import Model, KaldiRecognizer
import time

def test_wake_word():
    # Initialize PyAudio
    audio = pyaudio.PyAudio()
    
    # Audio parameters
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    
    # Load Vosk model
    model_path = "my_assistant/models/vosk-model-small-en-us-0.15"
    if not os.path.exists(model_path):
        print(f"Error: Vosk model not found at {model_path}")
        print("Please download the model from https://alphacephei.com/vosk/models")
        print("and extract it to the models directory")
        return
    
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, RATE)
    
    print("Starting wake word detection test...")
    print("Say 'hey jarvis' to trigger the wake word")
    print("Press Ctrl+C to exit")
    
    try:
        # Open audio stream
        stream = audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK
        )
        
        print("Listening...")
        
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                if result.get("text", "").lower() == "hey kashvi":
                    print("\nWake word detected!")
                    print("Text:", result["text"])
                    print("Confidence:", result.get("confidence", "N/A"))
                    print("\nListening...")
            
            # Print partial results
            partial = json.loads(recognizer.PartialResult())
            if partial.get("partial", ""):
                print(f"\rPartial: {partial['partial']}", end="", flush=True)
    
    except KeyboardInterrupt:
        print("\nTest stopped by user")
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

if __name__ == "__main__":
    test_wake_word() 