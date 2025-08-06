
import os
from google.cloud import texttospeech

def generate_audio(text: str, output_filename: str):
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Voice selection: Japanese, female voice
    voice = texttospeech.VoiceSelectionParams(
        language_code="ja-JP",
        name="ja-JP-Wavenet-A", # A female voice
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )

    # Audio configuration
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    # Save the audio to a file
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
        print(f"Audio content written to file {output_filename}")

if __name__ == '__main__':
    # For testing purposes
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/google_credentials.json" # Replace with your actual path
    sample_text = "AI技術の進化が目覚ましいです。"
    generate_audio(sample_text, "test_audio.mp3")


