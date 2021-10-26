import queue
import threading
import time
import speech_recognition as sr

def main(q):
    r = sr.Recognizer()
    mic = sr.Microphone()

    while True:
        try:
            with mic as source:
                r.adjust_for_ambient_noise(source) #雑音対策
                audio = r.listen(source)
            
            result = r.recognize_google(audio, language='ja-JP')
            print("[[voice recognition]]", result)
            q.put(result)

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
