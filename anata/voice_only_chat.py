import os, sys
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

from speech.scripts.speech import Speech
from recog.recog import Recognition
from chat.chat_client import ChatClient

chat = ChatClient()
recog = Recognition()
speech = Speech()

continue_flag = True
while continue_flag:
    prompt = recog.recognition()
    print("🗣️ :", prompt)
    if prompt == "終了":
        continue_flag = False
    if prompt == None:
        continue
    response = chat.make_response(prompt)
    print("💻 :", response)
    file, pseq, duration = speech.get_wav_file(response)
    print(file, pseq, duration)
    speech.play(file, block=True)

