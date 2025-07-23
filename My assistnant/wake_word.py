import pyaudio
import struct
import config
import os
import pvporcupine

class WakeWordDetector:
    def __init__(self):
        """Initialize the wake word detector with Porcupine."""
        # Initialize audio
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=config.CHANNELS,
            rate=config.SAMPLE_RATE,
            input=True,
            frames_per_buffer=config.CHUNK_SIZE
        )
        
        # Initialize Porcupine
        try:
            self.porcupine = pvporcupine.create(
                access_key="F9oXcpHCx+RCnaTjT3UP+cDpQq3UQwTDj5mae6Vyg59vpK1LeMqiIw==",
                keywords=[config.WAKE_WORD.lower()]
            )
            print(f"Porcupine initialized with wake word: {config.WAKE_WORD}")
        except Exception as e:
            raise Exception(f"Failed to initialize Porcupine: {str(e)}")

    def listen(self):
        """
        Listen for the wake word.
        Returns True when wake word is detected.
        """
        try:
            while True:
                # Read audio data
                pcm = self.stream.read(self.porcupine.frame_length, exception_on_overflow=False)
                pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
                
                # Process with Porcupine
                keyword_index = self.porcupine.process(pcm)
                
                # Check if wake word was detected
                if keyword_index >= 0:
                    print(f"Wake word '{config.WAKE_WORD}' detected!")
                    return True
                    
        except KeyboardInterrupt:
            self.cleanup()
            return False
        except Exception as e:
            print(f"Error in wake word detection: {str(e)}")
            self.cleanup()
            return False

    def cleanup(self):
        """Clean up resources."""
        if hasattr(self, 'stream'):
            self.stream.close()
        if hasattr(self, 'audio'):
            self.audio.terminate()
        if hasattr(self, 'porcupine'):
            self.porcupine.delete()

if __name__ == "__main__":
    # Test wake word detection
    detector = WakeWordDetector()
    print(f"Listening for wake word '{config.WAKE_WORD}'...")
    if detector.listen():
        print("Wake word detected!")
    detector.cleanup() 