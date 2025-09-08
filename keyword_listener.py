import os
import sounddevice as sd
import queue
import vosk
import json
import threading
from playsound import playsound


class KeywordListener:
    def __init__(self, keyword, activation_callback):
        self.keyword = keyword
        self.activation_callback = activation_callback
        self.q = queue.Queue()
        model_path = os.path.join(os.path.dirname(__file__), "vosk-model-small-en-us-0.15")
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model path '{model_path}' does not exist.")
        self.model = vosk.Model(model_path)

    def callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.q.put(bytes(indata))

    def listen_for_keyword(self):
        try:
            with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                                   channels=1, callback=self.callback):
                rec = vosk.KaldiRecognizer(self.model, 16000)
                while True:
                    data = self.q.get()
                    if rec.AcceptWaveform(data):
                        result = rec.Result()
                        text = json.loads(result).get('text', '')
                        if self.keyword in text:
                            self.play_notification_sound()
                            self.activation_callback()
        except Exception as e:
            print(f"Error in listen_for_keyword: {e}")

    def play_notification_sound(self):
        sound_path = os.path.join(os.path.dirname(__file__), "起動音.mp3")
        if os.path.exists(sound_path):
            try:
                playsound(sound_path)
            except Exception as e:
                print(f"Error playing sound: {e}")
        else:
            print(f"Sound file '{sound_path}' does not exist.")


if __name__ == "__main__":
    def activation_callback():
        print("Keyword detected!")


    listener = KeywordListener("friday", activation_callback)
    listener_thread = threading.Thread(target=listener.listen_for_keyword)
    listener_thread.daemon = True
    listener_thread.start()
    listener_thread.join()
