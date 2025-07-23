import pyttsx3
import config

class Speaker:
    def __init__(self):
        """Initialize the text-to-speech engine."""
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', config.VOICE_RATE)
        self.engine.setProperty('volume', config.VOICE_VOLUME)
        
        # Get available voices and set the default voice
        voices = self.engine.getProperty('voices')
        if voices:
            self.engine.setProperty('voice', voices[config.VOICE_ID].id)

    def speak(self, text):
        """
        Convert text to speech and play it.
        
        Args:
            text (str): The text to be spoken
        """
        try:
            print(f"Speaking: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Error during text-to-speech: {e}")

    def cleanup(self):
        """Clean up the text-to-speech engine."""
        try:
            self.engine.stop()
        except:
            pass

if __name__ == "__main__":
    # Test text-to-speech
    speaker = Speaker()
    speaker.speak("Hello! I am Nova, your privacy-focused voice assistant.")
    speaker.cleanup() 