FROM python:3.8-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install system dependencies required for audio playback
RUN apt-get update && apt-get install -y --no-install-recommends \
    libsdl2-2.0-0 \
    libsdl2-mixer-2.0-0 \
    alsa-utils \
    libasound2-dev \
    portaudio19-dev \
    libpulse-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /app

# Copy the client package files
COPY . /app/

# Install the package
RUN pip install --no-cache-dir -e .

# Create a non-root user to run the application
RUN useradd -m appuser
USER appuser

# Set the entrypoint to the example script
ENTRYPOINT ["python", "example.py"]

# Provide default command line arguments (can be overridden)
CMD ["--text", "Hello, welcome to the text to speech service!", "--play"]

