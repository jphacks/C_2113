import queue
import threading
import time
import speech_recognition as sr

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../common'))
from interface_struct import ListeningData


def main(q):
    print("[[VOICE RECOGNITION]]", "speech recognition start.")
    r = sr.Recognizer()
    mic = sr.Microphone()

    while True:
        try:
            with mic as source:
                r.adjust_for_ambient_noise(source) #雑音対策
                audio = r.listen(source)
            
            result = r.recognize_google(audio, language='ja-JP')
            print("[[VOICE RECOGNITION]]", result)
            q.put(ListeningData(txt=result, is_final=True))

        # 以下は認識できなかったときに止まらないように。
        except sr.UnknownValueError:
            continue
        except sr.RequestError as e:
            continue

if __name__ == '__main__':
    q = queue.Queue()
    def loop(q):
        while True:
            if q.empty():
                time.sleep(0.1)
                continue
            print("result:", q.get())
    t = threading.Thread(target=lambda:loop(q))
    t.start()
    main(q)
