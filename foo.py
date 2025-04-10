from tts_client import TTSClient

# Initialize the client
client = TTSClient("http://localhost:5000")

# Convert text to speech and play it
client.say("Hello, world!")

# Convert text to speech and save it to a file
client.text_to_speech("Hello, this is a test.", output_file="test.wav")
