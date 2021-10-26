import queue
from threading import Thread
import time

import gui
import voice_recognition
import input_page

def main():
    # 入力画面
    #  入力内容リスト(List[InputForm])を作ると良い
    input_data = input_page.main()

    # Button Dataの作成
    buttons = []
    for i in range(18):
        buttons.append(gui.ButtonData("人数", [f'{i}人でお願いします' for i in range(18)]))

    # 共有変数の作成
    speak = queue.Queue()
    listen = queue.Queue()

    # 音声認識の呼び出し
    vrec_thread = Thread(target=lambda:voice_recognition.main(listen))
    vrec_thread.start()

    # ttsの関数
    tts = print     # TODO

    # メイン画面の呼び出し
    root = gui.main(tts, buttons, speak, listen)
    root.mainloop() # ここで待機


def test_gui_integration():
    buttons = []
    for i in range(18):
        buttons.append(gui.ButtonData("人数", [f'{i}人でお願いします' for i in range(18)]))

        
    speak = queue.Queue()
    listen = queue.Queue()

    root = gui.main(print, buttons, speak, listen)

    def tester():
        script = [
            ["はい、こちら応物ピザ本郷店でございます",1.5],
            ["出前をお願いしたいのですが", 1],
            ["かしこまりました。\nメニューはいかがされますか？", 1.2],
            ["マルチンゲールのLサイズでお願いします", 1.5],
            ["かしこまりました", 1.3],
        ]
        time.sleep(3.0)
        for i,comment in enumerate(script):
            if (i%2)==0:
                listen.put(comment[0])
            else:
                speak.put(gui.SpeakingData(txt=comment[0], sec=comment[1]))
            time.sleep(comment[1])
        print("[[TESTER]] test function end.")

    t = Thread(target=tester)
    t.start()

    root.mainloop()

if __name__ == '__main__':
   main() 
