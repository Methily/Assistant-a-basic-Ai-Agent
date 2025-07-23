import time
from tasks.agent_router import handle_input
import datetime
import subprocess
from wake_word import WakeWordDetector
from speech_to_text import SpeechRecognizer
from llama_request import LlamaClient
from speak import Speaker
from tasks.google_calendar import GoogleCalendar
from tasks.notion_notes import NotionClient
from tasks.gmail import GmailClient
import config

class JarvisAssistant:
    def __init__(self):
        """Initialize all components of the voice assistant."""
        print("Initializing Jarvis Assistant...")
        
        # Core components
        self.wake_word_detector = WakeWordDetector()
        self.speech_recognizer = SpeechRecognizer()
        self.llama_client = LlamaClient()
        self.speaker = Speaker()
        
        # Task-specific components
        self.calendar = GoogleCalendar()
        self.notion = NotionClient()
        self.gmail = GmailClient()
        
        print("Jarvis Assistant initialized and ready!")

    def _parse_datetime(self, time_str):
        """
        Parse datetime string into datetime object.
        Returns None if parsing fails.
        """
        if not time_str:
            return None
            
        try:
            # Try parsing ISO format first
            return datetime.datetime.fromisoformat(time_str)
        except ValueError:
            try:
                # Try parsing common formats
                formats = [
                    "%Y-%m-%d %H:%M:%S",
                    "%Y-%m-%d %H:%M",
                    "%Y-%m-%d",
                    "%H:%M",
                    "%I:%M %p",
                    "%I:%M%p"
                ]
                
                for fmt in formats:
                    try:
                        return datetime.datetime.strptime(time_str, fmt)
                    except ValueError:
                        continue
                        
                return None
            except Exception:
                return None

    def _validate_calendar_params(self, params):
        """
        Validate and process calendar parameters.
        Returns a tuple of (is_valid, error_message, processed_params)
        """
        if not params:
            return False, "No parameters provided", None
            
        summary = params.get("summary")
        if not summary:
            return False, "No event title provided", None
            
        start_time = self._parse_datetime(params.get("start_time"))
        if not start_time:
            return False, "Could not understand the start time. Please specify when the event should start.", None
            
        # If end_time is not provided, default to 1 hour after start_time
        end_time = self._parse_datetime(params.get("end_time"))
        if not end_time:
            end_time = start_time + datetime.timedelta(hours=1)
            
        # Ensure end_time is after start_time
        if end_time <= start_time:
            return False, "End time must be after start time", None
            
        return True, None, {
            "summary": summary,
            "start_time": start_time,
            "end_time": end_time,
            "description": params.get("description"),
            "attendees": params.get("attendees")
        }

    def handle_command(self, command):
        """
        Process a command using the agent router.
        
        Args:
            command (str): The user's command
        """
        try:
            # Use the agent router to handle the command
            result = handle_input(command)
            return result
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"

    def run(self):
        """Main loop for the voice assistant."""
        print(f"Listening for wake word '{config.WAKE_WORD}'...")
        print("Say 'sleep' or 'shut down' to stop the assistant.")
        
        try:
            while True:
                # Wait for wake word
                if self.wake_word_detector.listen():
                    self.speaker.speak("Yes?")
                    
                    # Listen for command
                    command = self.speech_recognizer.listen()
                    if command:
                        # Check if user wants to sleep
                        command_lower = command.lower().strip()
                        if any(phrase in command_lower for phrase in ["sleep", "shut down", "shutdown", "stop", "goodbye", "bye"]):
                            self.speaker.speak("Goodbye! Shutting down.")
                            print("\nShutting down Jarvis Assistant...")
                            break
                            
                        # Process command and get response
                        response = self.handle_command(command)
                        self.speaker.speak(response)
                    
                    time.sleep(1)  # Brief pause before listening for wake word again
                    
        except KeyboardInterrupt:
            print("\nShutting down Jarvis Assistant...")
        finally:
            self.cleanup()

    def cleanup(self):
        """Clean up resources."""
        self.wake_word_detector.cleanup()
        self.speaker.cleanup()

    def main():
        while True:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                break

            response = handle_input(user_input)
            print("Agent:", response)

if __name__ == "__main__":
    '''subprocess.run(["models/llama.cpp/build/bin/Release/llama-server.exe", "-m", "C:/Users/methi/OneDrive/Desktop/CODING/assistent/tinyllama-1.1b-chat-v1.0.Q2_K.gguf"])'''
    assistant = JarvisAssistant()
    assistant.run() 