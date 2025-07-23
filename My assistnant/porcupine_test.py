import pyaudio
import struct
import pvporcupine
import config
import os
import speech_recognition as sr
import time

def listen_for_command():
    """Listen for a command after wake word is detected."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening for command...")
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        try:
            command = recognizer.recognize_google(audio).lower()
            print(f"Command received: {command}")
            return command
        except sr.UnknownValueError:
            print("Could not understand the command")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None

def test_wake_word():
    # Initialize PyAudio
    audio = pyaudio.PyAudio()
    
    # Audio parameters
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    
    try:
        # Initialize Porcupine
        porcupine = pvporcupine.create(
            access_key="F9oXcpHCx+RCnaTjT3UP+cDpQq3UQwTDj5mae6Vyg59vpK1LeMqiIw==",
            keywords=[config.WAKE_WORD.lower()]
        )
        print(f"Porcupine initialized with wake word: {config.WAKE_WORD}")
        
        # Open audio stream
        stream = audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )
        
        print("\nStarting wake word detection test...")
        print(f"Say '{config.WAKE_WORD}' to trigger the wake word")
        print("Press Ctrl+C to exit")
        print("\nListening...")
        
        while True:
            # Read audio data
            pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            
            # Process with Porcupine
            keyword_index = porcupine.process(pcm)
            
            # Check if wake word was detected
            if keyword_index >= 0:
                print(f"\nWake word '{config.WAKE_WORD}' detected!")
                
                # Listen for command
                command = listen_for_command()
                
                if command:
                    # Process the command
                    if any(word in command for word in config.COMMAND_PATTERNS["calendar"]):
                        print("Processing calendar command...")
                    elif any(word in command for word in config.COMMAND_PATTERNS["notion"]):
                        print("Processing Notion command...")
                    elif any(word in command for word in config.COMMAND_PATTERNS["email"]):
                        print("Processing email command...")
                    else:
                        print("Command not recognized")
                
                print("\nListening for wake word...")
    
    except KeyboardInterrupt:
        print("\nTest stopped by user")
    except Exception as e:
        print(f"\nError: {str(e)}")
    finally:
        if 'stream' in locals():
            stream.close()
        if 'audio' in locals():
            audio.terminate()
        if 'porcupine' in locals():
            porcupine.delete()

if __name__ == "__main__":
    test_wake_word() 