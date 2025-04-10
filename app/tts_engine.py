"""
TTS Engine using Coqui TTS for speech synthesis.
"""
from enum import Enum
import io
import logging
import os
import tempfile
from typing import Tuple, Optional, Dict, List

import numpy as np
from pydub import AudioSegment

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Language(str, Enum):
    """Supported languages for TTS."""
    ENGLISH = "en"
    SPANISH = "es"
    FRENCH = "fr"
    GERMAN = "de"
    ITALIAN = "it"
    PORTUGUESE = "pt"
    CHINESE = "zh"
    JAPANESE = "ja"
    KOREAN = "ko"
    RUSSIAN = "ru"


class OutputFormat(str, Enum):
    """Supported output formats for audio."""
    WAV = "WAV"
    MP3 = "MP3"


class TTSError(Exception):
    """Exception raised for errors in the TTS engine."""
    pass


class TTSEngine:
    """Text-to-Speech Engine using Coqui TTS."""
    
    def __init__(self):
        """Initialize the TTS engine and load models."""
        try:
            from TTS.api import TTS
            self.TTS = TTS
            self.models: Dict[Language, object] = {}
            self.available_models: Dict[Language, List[str]] = self._get_available_models()
            
            logger.info("TTS Engine initialized successfully")
        except ImportError as e:
            logger.error(f"Failed to import TTS: {str(e)}")
            raise TTSError(f"Failed to initialize TTS engine: {str(e)}")
        except Exception as e:
            logger.error(f"Failed to initialize TTS engine: {str(e)}", exc_info=True)
            raise TTSError(f"Failed to initialize TTS engine: {str(e)}")
    
    def _get_available_models(self) -> Dict[Language, List[str]]:
        """Get available models for each supported language."""
        try:
            available_models = {}
            
            # Create a temporary TTS instance to list models
            tts = self.TTS()
            
            # Map language codes to available models
            for lang in Language:
                available_models[lang] = [
                    model for model in tts.list_models() 
                    if f"_{lang.value}_" in model or f"/{lang.value}/" in model
                ]
            
            # Always ensure we have at least one model for English
            if not available_models[Language.ENGLISH]:
                available_models[Language.ENGLISH] = ["tts_models/en/ljspeech/vits"]
            
            return available_models
        except Exception as e:
            logger.error(f"Failed to get available models: {str(e)}", exc_info=True)
            # Fallback to default English model
            return {
                Language.ENGLISH: ["tts_models/en/ljspeech/vits"]
            }
    
    def _load_model(self, language: Language, voice: Optional[str] = None) -> None:
        """
        Load TTS model for the specified language.
        
        Args:
            language: The language to use
            voice: Optional voice model name to use
        """
        if language in self.models:
            return
        
        try:
            # If specific voice is provided and available, use it
            if voice and voice in self.available_models.get(language, []):
                model_name = voice
            # Otherwise use the first available model for the language
            elif language in self.available_models and self.available_models[language]:
                model_name = self.available_models[language][0]
            # Fallback to English if the language is not supported
            elif language != Language.ENGLISH and Language.ENGLISH in self.available_models:
                logger.warning(f"No model available for {language.value}, falling back to English")
                model_name = self.available_models[Language.ENGLISH][0]
            else:
                # Last resort, use the default English model
                logger.warning("No specific language model found, using default English TTS model")
                model_name = "tts_models/en/ljspeech/vits"
            
            logger.info(f"Loading TTS model: {model_name}")
            # Initialize the TTS model with the correct method
            tts = self.TTS(model_name=model_name)
            self.models[language] = tts
        
        except Exception as e:
            logger.error(f"Failed to load TTS model for {language.value}: {str(e)}", exc_info=True)
            raise TTSError(f"Failed to load TTS model for {language.value}: {str(e)}")
    
    def synthesize_speech(
        self, 
        text: str, 
        language: Language = Language.ENGLISH,
        output_format: OutputFormat = OutputFormat.WAV,
        voice: Optional[str] = None
    ) -> Tuple[bytes, str]:
        """
        Synthesize speech from text.
        
        Args:
            text: The text to convert to speech
            language: The language of the text
            output_format: The desired output format (WAV or MP3)
            voice: Optional specific voice model to use
            
        Returns:
            Tuple of (audio_data, content_type)
        """
        if not text:
            raise TTSError("Text cannot be empty")
        
        try:
            # Load model if not already loaded
            self._load_model(language, voice)
            tts = self.models.get(language)
            
            if not tts:
                raise TTSError(f"No TTS model available for language: {language.value}")
            
            # Create a temporary WAV file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
                temp_wav_path = temp_wav.name
            
            logger.info(f"Synthesizing speech for text: {text[:50]}{'...' if len(text) > 50 else ''}")
            
            # Generate speech using the new API
            wav = tts.tts(text=text)
            
            # Convert list to numpy array for proper audio processing
            wav = np.array(wav)
            
            # Save the generated audio to the temporary file
            try:
                import scipy.io.wavfile as wav_file
                wav_file.write(temp_wav_path, 22050, wav)
            except Exception as e:
                os.unlink(temp_wav_path)
                logger.error(f"Failed to save WAV file: {str(e)}", exc_info=True)
                raise TTSError(f"Failed to save WAV file: {str(e)}")
            
            # Convert to the desired format if needed
            if output_format == OutputFormat.MP3:
                audio = AudioSegment.from_wav(temp_wav_path)
                
                with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_mp3:
                    temp_mp3_path = temp_mp3.name
                
                audio.export(temp_mp3_path, format="mp3")
                
                with open(temp_mp3_path, "rb") as f:
                    audio_data = f.read()
                
                content_type = "audio/mpeg"
                os.unlink(temp_mp3_path)
            else:
                with open(temp_wav_path, "rb") as f:
                    audio_data = f.read()
                
                content_type = "audio/wav"
            
            # Clean up temporary file
            os.unlink(temp_wav_path)
            
            return audio_data, content_type
        
        except TTSError:
            raise
        except Exception as e:
            logger.error(f"Speech synthesis failed: {str(e)}", exc_info=True)
            raise TTSError(f"Speech synthesis failed: {str(e)}")

