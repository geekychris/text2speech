# TTS Client

A Python client for interacting with Text-to-Speech services. This client allows you to convert text to speech, play audio directly, and save audio files in different formats.

## Description

TTS Client provides a simple and intuitive interface to text-to-speech services. It handles the communication with the TTS server, processes the audio data, and provides utilities for playing and saving the generated speech.

### Features

- Text-to-speech conversion
- Direct audio playback
- Support for saving audio in MP3 and WAV formats
- Multiple language and voice support
- Error handling and retry mechanisms
- Simple and easy-to-use API

## Installation

### Prerequisites

- Python 3.6 or higher
- pip package manager

### Using pip

```bash
# Install from PyPI
pip install tts-client

# Or install from the source
git clone https://github.com/yourusername/tts-client.git
cd tts-client
pip install -e .
```

### Using Docker

```bash
# Pull the image
docker pull yourusername/tts-client:latest

# Or build from Dockerfile
git clone https://github.com/yourusername/tts-client.git
cd tts-client
docker build -t tts-client .
```

## Usage Examples

### Basic Usage

```python
from tts_client import TTSClient

# Initialize the client
client = TTSClient("http://localhost:5000")

# Convert text to speech and play it
client.say("Hello, world!")

# Convert text to speech and save it to a file
client.text_to_speech("Hello, this is a test.", output_file="test.mp3")
```

### Using Different Languages

```python
from tts_client import TTSClient

client = TTSClient("http://localhost:5000")

# English
client.say("Hello, how are you?", language="en-US")

# Spanish
client.say("Hola, ¿cómo estás?", language="es-ES")

# Get available languages
languages = client.get_available_languages()
print("Available languages:", languages)
```

### Error Handling

```python
from tts_client import TTSClient, TTSError

client = TTSClient("http://localhost:5000")

try:
    client.say("Hello, world!")
except TTSError as e:
    print(f"TTS Error: {e}")
except ConnectionError:
    print("Could not connect to the TTS server")
```

## API Reference

### TTSClient

```python
TTSClient(server_url, timeout=10)
```

#### Parameters:
- `server_url` (str): URL of the TTS server
- `timeout` (int, optional): Request timeout in seconds. Default is 10.

#### Methods:

**text_to_speech(text, language='en-US', voice=None, output_file=None, format='mp3')**

Converts text to speech and optionally saves it to a file.

- `text` (str): Text to convert to speech
- `language` (str, optional): Language code (e.g., 'en-US', 'es-ES'). Default is 'en-US'.
- `voice` (str, optional): Voice ID to use. Default is None (uses server default).
- `output_file` (str, optional): File path to save the audio. Default is None.
- `format` (str, optional): Audio format ('mp3' or 'wav'). Default is 'mp3'.

Returns: Bytes containing audio data.

**say(text, language='en-US', voice=None)**

Converts text to speech and plays it immediately.

- `text` (str): Text to convert to speech and play
- `language` (str, optional): Language code. Default is 'en-US'.
- `voice` (str, optional): Voice ID to use. Default is None.

Returns: None

**get_available_languages()**

Returns a list of available language codes.

Returns: List of strings containing language codes.

**get_available_voices(language=None)**

Returns a list of available voices, optionally filtered by language.

- `language` (str, optional): Language code to filter voices. Default is None.

Returns: List of voice IDs.

## Requirements

- Python 3.6+
- requests
- pygame

## Docker Setup

### Building the Docker Image

```bash
# Clone the repository
git clone https://github.com/yourusername/tts-client.git
cd tts-client

# Build the Docker image
docker build -t tts-client .
```

### Running the Docker Container

```bash
# Run the container with an example
docker run --rm tts-client python example.py

# Mount a volume to save audio files
docker run --rm -v $(pwd)/output:/app/output tts-client python -c "from tts_client import TTSClient; client = TTSClient('http://host.docker.internal:5000'); client.text_to_speech('Hello from Docker', output_file='/app/output/test.mp3')"
```

### Docker Compose

You can also use Docker Compose to run the TTS client along with the TTS server.

Create a `docker-compose.yml` file:

```yaml
version: '3'
services:
  tts-server:
    image: tts-server:latest
    ports:
      - "5000:5000"
  
  tts-client:
    image: tts-client:latest
    depends_on:
      - tts-server
    environment:
      - TTS_SERVER_URL=http://tts-server:5000
```

Run with Docker Compose:

```bash
docker-compose up
```

## Troubleshooting

### Cannot connect to the TTS server

- Check if the server URL is correct.
- Verify that the server is running and accessible.
- If using Docker, ensure that network settings are properly configured.

### Audio not playing

- Check if pygame is properly installed.
- Verify that your system has audio output devices configured.
- Try saving the audio to a file first, then play it with another player.

### Unsupported audio format

- The client supports MP3 and WAV formats. Make sure you're specifying one of these formats.
- Verify that the server supports the requested format.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

```
MIT License

Copyright (c) 2023 Your Name or Organization

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

