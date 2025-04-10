"""
FastAPI service for text-to-speech conversion.
"""
from enum import Enum
import logging
import os
from typing import Optional

from fastapi import FastAPI, HTTPException, Response, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
import uvicorn

from .tts_engine import TTSEngine, TTSError, Language, OutputFormat

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize the FastAPI app
app = FastAPI(
    title="Text-to-Speech API",
    description="API for converting text to speech using Coqui TTS",
    version="1.0.0",
)

# Create output directory for audio files if it doesn't exist
os.makedirs("output", exist_ok=True)


class TextToSpeechRequest(BaseModel):
    """Request model for text-to-speech conversion."""
    text: str = Field(..., min_length=1, max_length=5000, description="Text to convert to speech")
    language: Language = Field(default=Language.ENGLISH, description="Language for speech synthesis")
    output_format: OutputFormat = Field(default=OutputFormat.WAV, description="Audio output format")
    voice: Optional[str] = Field(default=None, description="Voice model to use (if None, default for language will be used)")


def get_tts_engine():
    """Dependency to get TTS engine instance."""
    return TTSEngine()


@app.get("/")
async def root():
    """Root endpoint for the API."""
    return {
        "message": "Text-to-Speech API is running",
        "endpoints": {
            "/tts": "POST - Convert text to speech",
            "/languages": "GET - List available languages",
        }
    }


@app.get("/languages")
async def list_languages():
    """Get a list of supported languages."""
    return {
        "languages": [lang.value for lang in Language],
        "default": Language.ENGLISH.value,
    }


@app.post("/tts")
async def text_to_speech(
    request: TextToSpeechRequest,
    tts_engine: TTSEngine = Depends(get_tts_engine)
):
    """
    Convert text to speech and return audio file.
    """
    logger.info(f"Received TTS request: language={request.language.value}, format={request.output_format.value}")
    logger.info(f"Text: {request.text[:50]}{'...' if len(request.text) > 50 else ''}")
    
    try:
        # Generate speech
        audio_content, content_type = tts_engine.synthesize_speech(
            text=request.text,
            language=request.language,
            output_format=request.output_format,
            voice=request.voice
        )
        
        logger.info(f"Successfully generated audio with size: {len(audio_content)} bytes")
        
        # Return the audio file
        return StreamingResponse(
            content=iter([audio_content]),
            media_type=content_type,
            headers={
                "Content-Disposition": f"attachment; filename=speech.{request.output_format.value.lower()}"
            }
        )
    
    except TTSError as e:
        logger.error(f"TTS Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected error occurred during speech synthesis")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

