"""
TTS Client - A Python client for Text-to-Speech services.

This module provides a client for interacting with Text-to-Speech services,
with support for converting text to speech, audio playback, and saving audio files.
"""

import os
import time
import tempfile
from typing import Optional, Literal, Union, Dict, Any
import requests
from requests.exceptions import RequestException
import pygame

# Initialize pygame mixer for audio playback
pygame.mixer.init()


class TTSClientError(Exception):
    """Base exception class for TTSClient errors."""
    pass


class TTSConnectionError(TTSClientError):
    """Exception raised when connection to the TTS server fails."""
    pass


class TTSConversionError(TTSClientError):
    """Exception raised when text-to-speech conversion fails."""
    pass


class TTSClient:
    """
    Client for Text-to-Speech service.
    
    This client provides methods to convert text to speech, play the resulting
    audio, and save it to a file.
    """
    
    def __init__(self, server_url: str):
        """
        Initialize the TTS client.
        
        Args:
            server_url: URL of the TTS server
        """
        self.server_url = server_url.rstrip('/')
        self._temp_files = []
        
    def __del__(self):
        """Clean up temporary files when the client is destroyed."""
        for temp_file in self._temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except Exception:
                pass
    
    def convert_text_to_speech(
        self, 
        text: str, 
        language: str = "en", 
        format: Literal["mp3", "wav"] = "mp3",
        voice: Optional[str] = None,
        **kwargs
    ) -> bytes:
        """
        Convert text to speech.
        
        Args:
            text: Text to convert to speech
            language: Language code (default: "en")
            format: Audio format ("mp3" or "wav")
            voice: Optional voice identifier
            **kwargs: Additional parameters to pass to the TTS service
            
        Returns:
            Audio data as bytes
            
        Raises:
            TTSConnectionError: If connection to TTS server fails
            TTSConversionError: If text-to-speech conversion fails
        """
        try:
            params: Dict[str, Any] = {
                "text": text,
                "language": language,
                "format": format
            }
            
            if voice:
                params["voice"] = voice
                
            # Add any additional parameters
            params.update(kwargs)
            
            response = requests.post(
                f"{self.server_url}/synthesize", 
                json=params,
                timeout=30
            )
            
            if response.status_code != 200:
                raise TTSConversionError(f"TTS service error: {response.status_code} - {response.text}")
                
            return response.content
            
        except RequestException as e:
            raise TTSConnectionError(f"Failed to connect to TTS server: {e}")
        except Exception as e:
            raise TTSConversionError(f"Text-to-speech conversion failed: {e}")
    
    def save_to_file(
        self, 
        text: str, 
        output_path: str, 
        language: str = "en", 
        format: Optional[Literal["mp3", "wav"]] = None,
        voice: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Convert text to speech and save to a file.
        
        Args:
            text: Text to convert to speech
            output_path: Path to save the audio file
            language: Language code (default: "en")
            format: Audio format (if None, determined from file extension)
            voice: Optional voice identifier
            **kwargs: Additional parameters to pass to the TTS service
            
        Returns:
            Path to the saved audio file
            
        Raises:
            TTSConnectionError: If connection to TTS server fails
            TTSConversionError: If text-to-speech conversion fails
            ValueError: If the format cannot be determined
        """
        # If format is not specified, try to determine from file extension
        if format is None:
            if output_path.lower().endswith('.mp3'):
                format = "mp3"
            elif output_path.lower().endswith('.wav'):
                format = "wav"
            else:
                raise ValueError(
                    "Cannot determine audio format from file extension. "
                    "Please specify format or use .mp3 or .wav file extension."
                )
        
        audio_data = self.convert_text_to_speech(
            text=text, 
            language=language, 
            format=format,
            voice=voice,
            **kwargs
        )
        
        with open(output_path, 'wb') as f:
            f.write(audio_data)
            
        return output_path
    
    def play(
        self, 
        text: str, 
        language: str = "en", 
        format: Literal["mp3", "wav"] = "mp3",
        voice: Optional[str] = None,
        **kwargs
    ) -> None:
        """
        Convert text to speech and play the audio.
        
        Args:
            text: Text to convert to speech
            language: Language code (default: "en")
            format: Audio format
            voice: Optional voice identifier
            **kwargs: Additional parameters to pass to the TTS service
            
        Raises:
            TTSConnectionError: If connection to TTS server fails
            TTSConversionError: If text-to-speech conversion fails
        """
        audio_data = self.convert_text_to_speech(
            text=text, 
            language=language, 
            format=format,
            voice=voice,
            **kwargs
        )
        
        # Create a temporary file to play
        suffix = f".{format}"
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as temp_file:
            temp_file.write(audio_data)
            temp_file_path = temp_file.name
            
        self._temp_files.append(temp_file_path)
        
        try:
            # Play the audio
            pygame.mixer.music.load(temp_file_path)
            pygame.mixer.music.play()
            
            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
                
        finally:
            # Clean up the temporary file
            try:
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)
                    self._temp_files.remove(temp_file_path)
            except Exception:
                pass
    
    def get_available_languages(self) -> Dict[str, str]:
        """
        Get a list of available languages from the TTS service.
        
        Returns:
            Dictionary mapping language codes to language names
            
        Raises:
            TTSConnectionError: If connection to TTS server fails
        """
        try:
            response = requests.get(
                f"{self.server_url}/languages",
                timeout=10
            )
            
            if response.status_code != 200:
                raise TTSConnectionError(f"Failed to get languages: {response.status_code} - {response.text}")
                
            return response.json()
            
        except RequestException as e:
            raise TTSConnectionError(f"Failed to connect to TTS server: {e}")
    
    def get_available_voices(self, language: Optional[str] = None) -> Dict[str, Any]:
        """
        Get available voices from the TTS service.
        
        Args:
            language: Optional language code to filter voices by language
            
        Returns:
            Dictionary of available voices
            
        Raises:
            TTSConnectionError: If connection to TTS server fails
        """
        try:
            params = {}
            if language:
                params["language"] = language
                
            response = requests.get(
                f"{self.server_url}/voices",
                params=params,
                timeout=10
            )
            
            if response.status_code != 200:
                raise TTSConnectionError(f"Failed to get voices: {response.status_code} - {response.text}")
                
            return response.json()
            
        except RequestException as e:
            raise TTSConnectionError(f"Failed to connect to TTS server: {e}")

