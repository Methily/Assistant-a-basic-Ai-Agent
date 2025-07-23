import speech_recognition as sr
import config

class SpeechRecognizer:
    def __init__(self):
        """Initialize the speech recognizer."""
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Adjust for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)

    def listen(self):
        """
        Listen for speech and convert to text.
        Returns the recognized text or None if recognition fails.
        """
        try:
            with self.microphone as source:
                print("Listening...")
                audio = self.recognizer.listen(source)
                
            print("Processing speech...")
            text = self.recognizer.recognize_google(audio)
            print(f"Recognized: {text}")
            return text.lower()
            
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None
        except Exception as e:
            print(f"Error during speech recognition: {e}")
            return None

if __name__ == "__main__":
    # Test speech recognition
    recognizer = SpeechRecognizer()
    text = recognizer.listen()
    if text:
        print(f"You said: {text}") 