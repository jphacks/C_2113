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
    add("何時から", int)
    add("持ち帰り", str)
    add("日付(月)", int)
    add("日付(日)", int)
    add("記念日", str)
    add("支払いカード", str)
    add("ポイント", str)
    input_data = input_page.main(input_list)

    # Button Dataの作成
    buttons = []
    add = lambda name,choices:buttons.append(gui.ButtonData(name, choices))
    ## 名前 1
    name = input_data["名前"]
    add("名前", [f"{name}と申します", f"{name}です", f"{name}ですけれども", f"{name}です、先日はお世話になりました"])
    ## 人数 2
    n = input_data["人数"]
    add("人数", [f"{n}人でお願いします", f"{n}人なのですがいけますか？", f"今のところ{n}人の予定です", f"{n}人です"])
    ## コース 3
    course = input_data["コース名"]
    add("コース", [f"{course}でお願いします", f"{course}でお願いしたいのですが",f"{course}で予約できますか"]) 
    ## 時間 4
    jikan = input_data["何時から"]
    add("時間", [f"{jikan}時からでお願いします", f"{jikan}時からでいけますか？", f"{jikan}時からで大丈夫でしょうか"])
    ## 持ち帰り 5
    take_out = input_data["持ち帰り"]
    add("持ち帰り", [f"持ち帰りで{take_out}をお願いします。",f"{take_out}の持ち帰りをお願いします。"])
    ## 日付 6
    month = input_data["日付(月)"]
    date = input_data["日付(日)"]
    add("日付", [f"{month}月{date}日でお願いします。",f"{month}月{date}日に予約したいです。",f"{month}月{date}日の予約は可能ですか"])
    ## 記念日 7
    aniversary = input_data["記念日"]
    add("誕生日", [f"{month}月{date}日は{aniversary}です。",f"{date}日は{aniversary}です。",f"{aniversary}をお祝いしたいと思っています。"])
    ## クレジットカード 8
    pay = input_data["支払いカード"]
    add("クレジットカード", [f"{pay}は使えますか？",f"{pay}で支払います。",f"{pay}加盟店ですか？"])
    ## ポイント Go to eat 9
    point = input_data["ポイント"]
    add("ポイント", [f"{point}は使えますか?",f"{point}対象店ですか？",f"{point}は貯まりますか？"])
    ## 10~14
    ##general(12のセリフ) 1~12
    for i in range(18-len(buttons)):
        buttons.append(gui.ButtonData("人数", [f'{i}人でお願いします' for i in range(18)]))

    add("挨拶",["おはようございます。","こんにちは。","夜分遅くに失礼します。",])
    add("急かす",["忙しいものですから、早い対応をお願いします。","時間がありませんので、なるべく早くお願いします。","早い時間におねがいします。"])
    add("社交辞令",["いつもお世話になっております。","ご丁寧にありがとうございます。"])
    add("相槌", ["よろしくお願いします。","少々お待ち下さい","大丈夫です。"])
    add("聞き直し",["よく聞こえませんでした。もう一度お聞きしてよろしいですか？","ちょっとよく聞こえなくて","Pardon?"])
    add("交代",["直接口頭でお話します。","家族が代わってくれるようなので、かわります。","ヘルパーさんがきてくれたのでかわります。"])
    add("時間(午前)", [f"{i}時からは空いてますか？" for i in [8,9,10,11,12]])
    add("時間(昼)", [f"{i}時からは空いてますか？" for i in [11,12,13,14,15,16]])
    add("時間(夕方)", [f"{i}時からは空いてますか？" for i in [14,15,16,17,18,19]])
    add("時間(夜)", [f"{i}時からは空いてますか？" for i in [18,19,20,21,22,23]])
    

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
