from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read() or "Text-to-Speech Client - A Python client for interacting with the Text-to-Speech Service"

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="tts_client",
    version="0.1.0",
    author="TTS Service Team",
    author_email="example@example.com",
    description="A Python client for the Text-to-Speech service that converts text to speech and provides audio playback",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/text-to-speech-service",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    keywords="text-to-speech, tts, audio, speech synthesis, client",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/text-to-speech-service/issues",
        "Documentation": "https://github.com/yourusername/text-to-speech-service#readme",
        "Source Code": "https://github.com/yourusername/text-to-speech-service",
    },
)

