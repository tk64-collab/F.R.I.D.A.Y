import sys
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QComboBox
from PyQt5.QtCore import pyqtSignal, QObject
from keyword_listener import KeywordListener
from speech_recognition_module import recognize_speech
from gpt_response import generate_response
from weather import get_weather
from news import get_news
from text_to_speech import text_to_speech, play_audio
from schedule import save_schedule, get_today_schedule

class Communicate(QObject):
    update_text = pyqtSignal(str, str)
    play_audio_signal = pyqtSignal(str)

class VoiceAssistantApp(QWidget):
    def __init__(self):
        super().__init__()
        self.comm = Communicate()
        self.comm.update_text.connect(self.update_text)
        self.comm.play_audio_signal.connect(self.play_audio_file)
        self.initUI()
        self.conversation_history = []

        self.keyword_listener = KeywordListener("friday", self.on_keyword_detected)
        self.listener_thread = threading.Thread(target=self.keyword_listener.listen_for_keyword)
        self.listener_thread.daemon = True
        self.listener_thread.start()

    def initUI(self):
        self.layout = QVBoxLayout()

        self.textEdit = QTextEdit(self)
        self.layout.addWidget(self.textEdit)

        self.modelComboBox = QComboBox(self)
        self.modelComboBox.addItems(["gpt-3.5-turbo", "gpt-4o"])
        self.layout.addWidget(self.modelComboBox)

        self.listenButton = QPushButton('Listen', self)
        self.listenButton.clicked.connect(self.listen_and_respond)
        self.layout.addWidget(self.listenButton)

        self.setLayout(self.layout)
        self.setWindowTitle('F.R.I.D.A.Y.')
        self.show()

    def listen_and_respond(self):
        threading.Thread(target=self.handle_listen_and_respond).start()

    def handle_listen_and_respond(self):
        try:
            print("handle_listen_and_respond start")
            question = recognize_speech()
            if question is None:
                return
            self.comm.update_text.emit(f"User: {question}", "user")
            self.conversation_history.append(question)

            if "天気" in question:
                answer = get_weather(question)
            elif "ニュース" in question:
                answer = get_news()
            elif "予定" in question:
                if "記録" in question:
                    event = question.replace("予定を記録して", "").strip()
                    save_schedule(event)
                    answer = f"予定「{event}」を記録しました。"
                elif "確認" in question:
                    schedule = get_today_schedule()
                    if schedule:
                        answer = "今日の予定は以下の通りです:\n" + "\n".join(schedule)
                    else:
                        answer = "今日の予定はありません。"
                else:
                    answer = "予定に関する具体的な操作を指示してください。例えば、「予定を記録して」または「予定を確認して」と言ってください。"
            elif "プログラム" in question:
                answer = "プログラムに関する質問ですね。どのようなコードが必要ですか？"
            else:
                model = self.modelComboBox.currentText()
                answer = generate_response(question, self.conversation_history, model)

            self.comm.update_text.emit(f"Assistant: {answer}", "assistant")
            self.conversation_history.append(answer)

            audio_path = text_to_speech(answer)
            self.comm.play_audio_signal.emit(str(audio_path))
            print("handle_listen_and_respond end")
        except Exception as e:
            print(f"Error in handle_listen_and_respond: {e}")

    def update_text(self, text, role):
        self.textEdit.append(text)

    def play_audio_file(self, file_path):
        play_audio(file_path)

    def on_keyword_detected(self):
        self.listen_and_respond()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = VoiceAssistantApp()
    sys.exit(app.exec_())
