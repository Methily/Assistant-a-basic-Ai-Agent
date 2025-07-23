# Privacy-Focused Voice Assistant

A privacy-focused voice assistant that runs completely offline, using local models and APIs. The assistant can help you manage your calendar, emails, and Notion workspace through voice commands.

## Features

- **Offline Voice Recognition**: Uses local models for wake word detection and speech recognition
- **Privacy-Focused**: All processing happens locally on your machine
- **Calendar Integration**: Manage your Google Calendar through voice commands
- **Email Management**: Handle your Gmail through voice commands
- **Notion Integration**: Interact with your Notion workspace through voice commands
- **Local LLM**: Uses llama.cpp for natural language understanding

## Prerequisites

- Python 3.8 or higher
- Google Cloud credentials (for Calendar and Gmail APIs)
- Notion API key and database ID
- Porcupine access key (for wake word detection)
- Local LLM model (e.g., tinyllama-1.1b-chat-v1.0.Q2_K.gguf)
- llama.cpp server running locally

note- before running the main.py file. Run the llama.cpp server locally(tinyllama file) first; then main.py.

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <project-directory>
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r my_assistant/requirements.txt
```

4. Place your credentials:
   - Google credentials: `my_assistant/credentials/google_credentials.json`
   - Notion API key and database ID: set as environment variables or in `.env`
   - Porcupine access key: set in `.env` or `config.py`

5. Place your LLM model (e.g., `tinyllama-1.1b-chat-v1.0.Q2_K.gguf`) in the project root or update the path in your llama.cpp server command.

6. Start the llama.cpp server (example):
```bash
# Adjust the path to your model as needed
./my_assistant/models/llama.cpp/build/bin/Release/llama-server.exe -m ../../../../tinyllama-1.1b-chat-v1.0.Q2_K.gguf
```

## Usage

1. Start the assistant:
```bash
python -m my_assistant.main
```

2. Say 'Jarvis' to activate the assistant.

3. Speak your command. For example:
   - "Schedule a meeting with John tomorrow at 2 PM"
   - "Check my calendar for next week"
   - "Send an email to Sarah about the project update"
   - "Create a new page in my Notion workspace"

## Project Structure

```
<project-directory>/
├── my_assistant/
│   ├── main.py                # Main application entry point
│   ├── config.py              # Configuration and constants
│   ├── wake_word.py           # Wake word detection using Porcupine
│   ├── speech_to_text.py      # Speech recognition using SpeechRecognition
│   ├── llama_request.py       # LLM processing using llama.cpp
│   ├── speak.py               # Text-to-speech (TTS)
│   ├── mic_test.py            # Microphone test script
│   ├── porcupine_test.py      # Porcupine wake word test script
│   ├── wake_word_test.py      # (Legacy) Wake word test script
│   ├── requirements.txt       # Python dependencies
│   ├── credentials/
│   │   ├── google_credentials.json
│   │   └── google_token.json
│   ├── tasks/
│   │   ├── agent_router.py    # Command routing and intent handling
│   │   ├── google_calendar.py # Google Calendar integration
│   │   ├── gmail.py           # Gmail integration
│   │   ├── notion_notes.py    # Notion notes integration
│   │   └── notion_tasks.py    # Notion tasks integration
│   └── models/
│       └── llama.cpp/         # llama.cpp source and model files
├── tinyllama-1.1b-chat-v1.0.Q2_K.gguf # Example LLM model
├── README.md                  # This file
└── mic_test.wav               # Example/test audio file
```

## Configuration

The assistant can be configured through the `my_assistant/config.py` file and environment variables (using a `.env` file is recommended):

- `PORCUPINE_ACCESS_KEY`: Your Porcupine access key
- `GOOGLE_CREDENTIALS_PATH`: Path to your Google Cloud credentials (default: `my_assistant/credentials/google_credentials.json`)
- `NOTION_API_KEY`: Your Notion API key
- `NOTION_DATABASE_ID`: Your Notion database ID
- `LLAMA_SERVER_URL`: URL of your local llama.cpp server (default: `http://localhost:8080/completion`)
- `COMMAND_PATTERNS`: Patterns for different types of commands

## Testing

- **Microphone Test:**
  ```bash
  python my_assistant/mic_test.py
  ```
  Use this to verify your microphone is working and to record a test audio file.

- **Wake Word Test (Porcupine):**
  ```bash
  python my_assistant/porcupine_test.py
  ```
  Use this to test wake word detection with Porcupine and your chosen wake word (default: 'jarvis').

- **Speech Recognition Test:**
  ```bash
  python my_assistant/speech_to_text.py
  ```
  Use this to test speech-to-text functionality.

## Notes

- Ensure all credentials and API keys are kept private and never committed to version control.
- You may need to adjust paths or environment variables depending on your OS and setup.
- For Google and Notion integrations, follow the official documentation to obtain API credentials.
- The wake word and assistant name can be changed in `config.py`.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [llama.cpp](https://github.com/ggerganov/llama.cpp) for the local LLM implementation
- [Porcupine](https://github.com/Picovoice/porcupine) for wake word detection
- [SpeechRecognition](https://github.com/Uberi/speech_recognition) for speech recognition
- [Google Calendar API](https://developers.google.com/calendar)
- [Gmail API](https://developers.google.com/gmail)
- [Notion API](https://developers.notion.com) 