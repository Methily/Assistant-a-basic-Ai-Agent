import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# LLM Configuration
LLAMA_SERVER_URL = "http://localhost:8080/completion"

# Wake word configuration
WAKE_WORD = "jarvis"  # You can change this to any wake word supported by Porcupine
PORCUPINE_ACCESS_KEY = "F9oXcpHCx+RCnaTjT3UP+cDpQq3UQwTDj5mae6Vyg59vpK1LeMqiIw=="  # Your Porcupine access key

# Google API Configuration
GOOGLE_CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), "credentials", "google_credentials.json")
GOOGLE_TOKEN_PATH = os.path.join(os.path.dirname(__file__), "credentials", "google_token.json")
GOOGLE_SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send"
]

# Notion API Configuration
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

# Audio Configuration
SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK_SIZE = 1024
FORMAT = "int16"

# Voice Configuration
VOICE_RATE = 150  # Speed of speech
VOICE_VOLUME = 1.0  # Volume (0.0 to 1.0)
VOICE_ID = 0  # Voice ID (0 for default)

# Command patterns for LLM
COMMAND_PATTERNS = {
    "calendar": ["schedule", "calendar", "event", "meeting", "appointment", "googlecalendar"],
    "notion": ["note", "todo", "task", "reminder", "notion"],
    "email": ["email", "mail", "gmail", "inbox", "unread"]
}

def get_google_credentials():
    """Load Google API credentials from the credentials file."""
    if not os.path.exists(GOOGLE_CREDENTIALS_PATH):
        raise FileNotFoundError(
            f"Google credentials file not found at {GOOGLE_CREDENTIALS_PATH}. "
            "Please download it from Google Cloud Console and place it in the credentials folder."
        )
    return GOOGLE_CREDENTIALS_PATH

def get_notion_client():
    """Initialize and return Notion client with API key."""
    if not NOTION_API_KEY:
        raise ValueError("Notion API key not found in environment variables")
    return NOTION_API_KEY 