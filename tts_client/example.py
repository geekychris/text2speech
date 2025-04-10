#!/usr/bin/env python3
"""
Example usage of the TTS Client

This script demonstrates the various features of the TTS client
including text-to-speech conversion, audio playback, saving to file,
language selection, and error handling.
"""

import os
import time
from tts_client import TTSClient

# Replace with your TTS server URL
TTS_SERVER_URL = "http://localhost:5000"

def main():
    print("TTS Client Example Script")
    print("=" * 50)
    
    # Initialize the client
    client = TTSClient(server_url=TTS_SERVER_URL)
    
    # Example 1: Basic text-to-speech conversion and playback
    print("\n1. Basic text-to-speech conversion and playback")
    try:
        print("Converting 'Hello, world!' to speech...")
        audio_data = client.text_to_speech("Hello, world!")
        print("Playing audio...")
        client.play_audio(audio_data)
        # Wait for audio to finish
        time.sleep(2)
    except Exception as e:
        print(f"Error in basic example: {e}")
    
    # Example 2: Saving audio to file
    print("\n2. Saving audio to file")
    try:
        print("Converting 'This is a test of saving audio to a file.' to speech...")
        audio_data = client.text_to_speech("This is a test of saving audio to a file.")
        filename = "example_output.mp3"
        print(f"Saving audio to {filename}...")
        client.save_audio(audio_data, filename)
        print(f"Audio saved successfully to {os.path.abspath(filename)}")
    except Exception as e:
        print(f"Error saving audio: {e}")
    
    # Example 3: Using different languages
    print("\n3. Using different languages")
    languages = {
        "English": "en",
        "Spanish": "es",
        "French": "fr",
        "German": "de",
        "Japanese": "ja"
    }
    
    for name, code in languages.items():
        try:
            print(f"Converting 'Hello' to {name}...")
            audio_data = client.text_to_speech("Hello", language=code)
            print(f"Playing {name} audio...")
            client.play_audio(audio_data)
            # Wait for audio to finish
            time.sleep(2)
        except Exception as e:
            print(f"Error with {name} conversion: {e}")
    
    # Example 4: Error handling
    print("\n4. Error handling demonstration")
    try:
        print("Attempting to convert with invalid language code...")
        client.text_to_speech("This will fail", language="invalid_language")
    except Exception as e:
        print(f"Successfully caught error: {e}")
    
    try:
        print("Attempting to connect to non-existent server...")
        invalid_client = TTSClient(server_url="http://nonexistent-server:9999")
        invalid_client.text_to_speech("This will fail")
    except Exception as e:
        print(f"Successfully caught connection error: {e}")
    
    # Example 5: Getting available languages and voices
    print("\n5. Getting available languages and voices")
    try:
        print("Fetching available languages...")
        languages = client.get_available_languages()
        print(f"Available languages: {languages}")
        
        print("\nFetching available voices...")
        voices = client.get_available_voices()
        print(f"Available voices: {voices}")
        
        # If voices for specific languages are supported
        try:
            english_voices = client.get_available_voices(language="en")
            print(f"\nAvailable English voices: {english_voices}")
        except Exception:
            print("Language-specific voice listing not supported by this server")
    except Exception as e:
        print(f"Error fetching languages/voices: {e}")
    
    # Example 6: Advanced usage - different voice and audio format
    print("\n6. Advanced usage - different voice and audio format")
    try:
        print("Converting text with specific voice and audio format...")
        audio_data = client.text_to_speech(
            "This is an example of using a specific voice and audio format.",
            language="en",
            voice="female1",  # Replace with an actual voice name from your server
            audio_format="wav"  # If your client supports different formats
        )
        print("Playing audio with specific voice...")
        client.play_audio(audio_data)
        # Wait for audio to finish
        time.sleep(3)
    except Exception as e:
        print(f"Error in advanced usage: {e}")
    
    print("\nExample script completed.")

if __name__ == "__main__":
    main()

