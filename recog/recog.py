import speech_recognition as sr

class Recognition:
    def __init__(self):
        self.listener = sr.Recognizer()
        self.microphone = sr.Microphone()


    def recognition(self, timeout=None):
        with self.microphone as source:
            try:
                self.listener.adjust_for_ambient_noise(source, duration=1)
                print("Listening...")
                voice = self.listener.listen(source,timeout=timeout)
                voice_text = self.listener.recognize_google(voice, language="ja-JP")
            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                pass
            finally:
                return voice_text
