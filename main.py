import queue
from threading import Thread
import time

import gui
import tts
import voice_recognition
import input_page

def get_input_list():
    input_list = []
    add = lambda name,type_:input_list.append(input_page.InputForm(name,type_))
    add("名前", str)
    add("人数", int)
    add("日付(月)", int)
    add("日付(日)", int)
    add("何時から", int)
    add("記念日", str)
    add("コース名", str)
    add("支払いカード", str)
    add("ポイント", str)
    add("子供の数", int)
    add("電話番号", int)
    add("苦手な食べ物", str)
    add("席の位置", str)
    return input_list

def get_test_input():
    dic = {}
    for input_form in get_input_list():
        if input_form.input_type is int:
            dic[input_form.label] = 1
        elif input_form.input_type is str:
            dic[input_form.label] = f"[{input_form.label}]"
    return dic

def call_input():
    # 入力画面
    input_list = get_input_list()
    return input_page.main(input_list)

def main(debug_mode = False, skip_input=False, tts_skip=False, stt_skip=False):
    if skip_input and debug_mode:
        print("[[MAIN]]", "skip input form")
        input_data = get_test_input()
    else:
        input_data = call_input()

    print("[[MAIN]] INPUT DATA is below.")
    print(input_data)
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
    add("時間(午前)", [f"{i}時からは空いてますか？" for i in [8,9,10,11,12]])
    add("時間(昼)", [f"{i}時からは空いてますか？" for i in [11,12,13,14,15,16]])
    add("時間(夕方)", [f"{i}時からは空いてますか？" for i in [14,15,16,17,18,19]])
    add("時間(夜)", [f"{i}時からは空いてますか？" for i in [18,19,20,21,22,23]])
    ## 日付 6
    month = input_data["日付(月)"]
    date = input_data["日付(日)"]
    add("日付", [f"{month}月{date}日の予約は可能ですか",f"{month}月{date}日でお願いします。",f"{month}月{date}日に予約したいです。"])
    ## 記念日 7
    aniversary = input_data["記念日"]
    add("誕生日", [f"{month}月{date}日は{aniversary}です。",f"{date}日は{aniversary}です。",f"{aniversary}をお祝いしたいと思っています。"])
    ## 電話番号 11
    phone = input_data["電話番号"]
    add("電話", [f"電話番号は{phone}なります。",f"電話番号は{phone}です。",f"ケータイは{phone}です。"])
    ## クレジットカード 8
    pay = input_data["支払いカード"]
    add("クレジットカード", [f"{pay}は使えますか？",f"{pay}で支払います。",f"{pay}加盟店ですか？"])
    ## ポイント Go to eat 9
    point = input_data["ポイント"]
    add("ポイント", [f"{point}は使えますか?",f"{point}対象店ですか？",f"{point}は貯まりますか？"])
    ## 子供 10
    children = input_data["子供の数"]
    add("子供", [f"子供が{children}人います。",f"{n}のうち子供が{children}です。",f"{children}人子供がいますが大丈夫ですか。"])
    ## 席の位置 12
    place = input_data["席の位置"]
    add("席",[f"席は{place}の近くでお願いします。",f"{place}近くに席をお願いします。",f"{place}側にお願いします。"])
    ## 苦手な食べ物 13
    hate = input_data["苦手な食べ物"]
    add("苦手",[f"{hate}は食べられません。",f"{hate}が入った食べ物は避けてください。",f"{hate}が嫌いです。"])



    add("その他",["おはようございます。","こんにちは。",
        "ご丁寧にありがとうございます。","よろしくお願いします。","ありがとうございます。",
        "助かります。","ありがとうございました。","失礼します。","少々お待ち下さい","大丈夫です。",
        "よく聞こえませんでした。もう一度お聞きしてよろしいですか？","ちょっとよく聞こえなくて","Pardon?",
        "直接口頭でお話します。","家族が代わってくれるようなので、かわります。","ヘルパーさんがきてくれたのでかわります。","夜分遅くに失礼します。","忙しいものですから、早い対応をお願いします。",
        "時間がありませんので、なるべく早くお願いします。","早い時間におねがいします。","いつもお世話になっております。"])


    # 共有変数の作成
    tts_queue = queue.Queue()
    speak = queue.Queue()
    listen = queue.Queue()

    # ttsの呼び出し
    tts_thread = Thread(target = lambda:tts.main(tts_queue, speak, tts_skip and debug_mode))
    tts_thread.start()

    # 音声認識の呼び出し
    if stt_skip and debug_mode:
        vrec_thread = Thread(target=lambda:voice_recognition.main(listen))
        vrec_thread.start()
    else:
        stt_thread = Thread(target = lambda:voice_recognition.stt_main(listen,True))
        stt_thread.start()

    # メイン画面の呼び出し
    print("[[MAIN]]", "call gui.main")
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
            ["はい、こちら応物ピザ",0.5, False],
            ["はい、こちら応物ピザ本郷店でございます",1.0, True],
            ["出前をお願いしたいのですが", 1],
            ["かしこまりました。", 0.6,False],
            ["かしこまりました。\nメニューはいかがされますか？", 0.6, True],
            ["マルチンゲールのLサイズでお願いします", 1.5],
            ["かしこまりました", 1.3],
        ]
        time.sleep(3.0)
        for comment in script:
            if len(comment) > 2:
                listen.put(gui.ListeningData(txt=comment[0], is_final=comment[2]))
            else:
                speak.put(gui.SpeakingData(txt=comment[0], sec=comment[1]))
            time.sleep(comment[1])
        print("[[TESTER]] test function end.")

    t = Thread(target=tester)
    t.start()

    root.mainloop()

if __name__ == '__main__': 
    main(debug_mode=True, skip_input=False, tts_skip=False, stt_skip=True) 



   # test_gui_integration()
