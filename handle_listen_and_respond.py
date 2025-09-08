def handle_listen_and_respond(self):
    try:
        print("handle_listen_and_respond start")
        question = recognize_speech()
        if question:
            self.comm.update_text.emit(f"User: {question}", "user")
            self.conversation_history.append({"role": "user", "content": question})

            if "天気" in question or "weather" in question.lower():
                # 特定のキーワードに続く地名を抽出
                location = None
                if "天気は" in question:
                    location = question.split("天気は")[-1].strip()
                elif "天気" in question:
                    location = question.split("天気")[-1].strip()
                elif "in" in question:
                    location = question.split("in")[-1].strip()

                if location:
                    print(f"Getting weather for location: {location}")
                    answer = get_weather(location)
                    print(f"Weather response: {answer}")
                else:
                    answer = "すみません、場所を特定できませんでした。"
            elif "プログラム" in question:
                answer = "プログラムに関する質問ですね。どのようなコードが必要ですか？"
            else:
                model = self.modelComboBox.currentText()
                answer = generate_response(question, self.conversation_history, model)

            self.comm.update_text.emit(f"Assistant: {answer}", "assistant")
            self.conversation_history.append({"role": "assistant", "content": answer})

            audio_path = text_to_speech(answer)
            self.comm.play_audio_signal.emit(str(audio_path))
            print("handle_listen_and_respond end")
        else:
            print("No input detected.")
    except Exception as e:
        print(f"Error in handle_listen_and_respond: {e}")
