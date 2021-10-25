from gui.gui_main import main as gui_main
from gui.button_data import ButtonData
import queue
from threading import Thread
import time

if __name__ == '__main__':
    buttons = []
    for i in range(18):
        buttons.append(ButtonData("人数", [f'{i}人でお願いします' for i in range(18)]))

        
    speak = queue.Queue()
    listen = queue.Queue()

    root = gui_main(print, buttons, speak, listen)

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
                speak.put(comment)
            time.sleep(comment[1])
        print("[[TESTER]] test function end.")

    t = Thread(target=tester)
    t.start()

    root.mainloop()

