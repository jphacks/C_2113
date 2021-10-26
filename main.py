import queue
from threading import Thread
import time

import gui
import voice_recognition
import input_page

def main():
    # 入力画面
    #  入力内容リスト(List[InputForm])を作ると良い
    input_list = []
    add = lambda name,type_:input_list.append(input_page.InputForm(name,type_))
    add("名前", str)
    add("人数", int)
    add("コース名", str)
    add("時間", int)
    input_data = input_page.main(input_list)

    # Button Dataの作成
    buttons = []
    add = lambda name,choices:buttons.append(gui.ButtonData(name, choices))
    ## 名前
    name = input_data["名前"]
    add("名前", [f"{name}と申します", f"{name}です", f"{name}ですけれども", f"{name}です、先日はお世話になりました"])
    ## 人数
    n = input_data["人数"]
    add("人数", [f"{n}人でお願いします", f"{n}人なのですがいけますか？", f"今のところ{n}人の予定です", f"{n}人です"])
    ## コース
    course = input_data["コース名"]
    add("コース", [f"{course}でお願いします", f"{course}でお願いしたいのですが"]) 
    ## 時間
    jikan = input_data["時間"]
    add("時間", [f"{jikan}時からでお願いします", f"{jikan}時からでいけますか？", f"{jikan}時からで大丈夫でしょうか"])
    ## その他
    add("時間(午前)", [f"{i}時からは空いてますか？" for i in [8,9,10,11,12]])
    add("時間(昼)", [f"{i}時からは空いてますか？" for i in [11,12,13,14,15,16]])
    add("時間(夕方)", [f"{i}時からは空いてますか？" for i in [14,15,16,17,18,19]])
    add("時間(夜)", [f"{i}時からは空いてますか？" for i in [18,19,20,21,22,23]])
    for i in range(18-len(buttons)):
        buttons.append(gui.ButtonData("人数", [f'{i}人でお願いします' for i in range(18)]))

    # 共有変数の作成
    tts_queue = queue.Queue()
    speak = queue.Queue()
    listen = queue.Queue()

    # 音声認識の呼び出し
    vrec_thread = Thread(target=lambda:voice_recognition.main(listen))
    vrec_thread.start()

    # ttsの呼び出し

    # メイン画面の呼び出し
    root = gui.main(tts_queue, buttons, speak, listen)
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
