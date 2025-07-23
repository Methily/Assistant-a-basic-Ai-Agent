import sounddevice as sd
import numpy as np
import wave
import os

def list_audio_devices():
    """List all available audio input devices."""
    devices = sd.query_devices()
    print("\nAvailable Audio Input Devices:")
    print("-" * 50)
    input_devices = []
    
    for i, device in enumerate(devices):
        if device['max_input_channels'] > 0:  # Only show devices that can record
            print(f"Device {i}: {device['name']}")
            print(f"  Type: Input Device")
            print(f"  Input channels: {device['max_input_channels']}")
            print(f"  Default sample rate: {device['default_samplerate']}")
            print("-" * 50)
            input_devices.append(i)
    
    if not input_devices:
        print("No input devices found! Please check your microphone connection.")
    return input_devices

def test_microphone(device_id=None, duration=5):
    """Test microphone recording for a specified duration."""
    try:
        # Get device info
        device_info = sd.query_devices(device_id, 'input')
        if device_info['max_input_channels'] == 0:
            raise ValueError("Selected device is not an input device")
            
        print(f"\nTesting microphone: {device_info['name']}")
        print(f"Sample rate: {device_info['default_samplerate']}")
        print(f"Channels: {device_info['max_input_channels']}")
        
        # Record audio
        print(f"\nRecording for {duration} seconds...")
        recording = sd.rec(
            int(duration * device_info['default_samplerate']),
            samplerate=int(device_info['default_samplerate']),
            channels=1,
            dtype='int16',
            device=device_id
        )
        sd.wait()
        
        # Save the recording
        output_file = "mic_test.wav"
        with wave.open(output_file, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # 2 bytes for int16
            wf.setframerate(int(device_info['default_samplerate']))
            wf.writeframes(recording.tobytes())
        
        print(f"\nRecording saved to {output_file}")
        print("Please play the file to verify the recording quality.")
        
        # Check recording levels
        max_level = np.max(np.abs(recording))
        print(f"\nRecording level: {max_level/32768*100:.1f}%")
        if max_level < 1000:
            print("WARNING: Recording level is very low. Please check your microphone settings.")
        elif max_level > 30000:
            print("WARNING: Recording level is very high. Consider lowering the input volume.")
        else:
            print("Recording level is good!")
            
    except Exception as e:
        print(f"Error testing microphone: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Make sure you selected an input device (microphone)")
        print("2. Check if your microphone is properly connected")
        print("3. Verify the microphone is not muted in Windows settings")
        print("4. Try selecting a different device number")

def main():
    print("Microphone Configuration Test")
    print("=" * 50)
    
    # List all audio devices
    input_devices = list_audio_devices()
    
    if not input_devices:
        return
    
    # Ask user to select a device
    while True:
        try:
            device_id = input("\nEnter the device number to test (or press Enter for default): ")
            if device_id.strip() == "":
                device_id = None
            else:
                device_id = int(device_id)
                if device_id not in input_devices:
                    print(f"Please select a valid input device number from the list above.")
                    continue
            break
        except ValueError:
            print("Please enter a valid number or press Enter for default device.")
    
    # Test the selected microphone
    test_microphone(device_id)

if __name__ == "__main__":
    main() 