from pathlib import Path
from openai import OpenAI
import os

# OpenAI APIキーを環境変数から取得
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

def text_to_speech(text, voice="nova", model="tts-1"):
    speech_file_path = Path(__file__).parent / "speech.mp3"
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=text
    )

    # ストリームされたオーディオデータをファイルに書き込む
    with open(speech_file_path, "wb") as audio_file:
        audio_file.write(response.content)

    return speech_file_path

def play_audio(file_path):
    os.system(f'afplay {file_path}')  # macOSのデフォルトプレイヤーで再生

if __name__ == "__main__":
    text = "Today is a wonderful day to build something people love!"
    audio_path = text_to_speech(text)
    play_audio(audio_path)
