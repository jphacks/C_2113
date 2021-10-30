import queue
from threading import Thread
import time

import gui
import tts
import voice_recognition
import input_page

def get_input_list():
    input_list = []
    def get(name, type_, default=None):
        if default is None:
            return input_page.InputForm(label=name, input_type=type_)
        if type_ is str:
            return input_page.InputForm(label=name, input_type=type_, default_str=default)
        elif type_ is int:
            return input_page.InputForm(label=name, input_type=type_, default_int=default)
        else:
            return input_page.InputForm(label=name, input_type=type_)
    add = lambda name,type_,default=None:input_list.append(get(name, type_, default))
    add("名前", str, "関")
    add("人数", int, 2)
    add("日付(月)", int, 11)
    add("日付(日)", int, 8)
    add("何時から", int, 19)
    add("記念日", str)
    add("コース名", str, "肉料理")
    add("支払いカード", str, "Visa")
    add("ポイント", str, "ポンタカード")
    add("電話番号", str, "03 1234 5678")
    add("アレルギー", str, "ピーナッツ")
    add("席の位置", str, "窓際")
    return input_list

def get_test_input():
    dic = {}
    for input_form in get_input_list():
        if input_form.input_type is int:
            dic[input_form.label] = input_form.default_int
        elif input_form.input_type is str:
            dic[input_form.label] = input_form.default_str
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
    ## 時間 4 ~ 8
    jikan = input_data["何時から"]
    add("時間", [f"{jikan}時からでお願いします", f"{jikan}時からでいけますか？", f"{jikan}時からで大丈夫でしょうか"])
    add("時間(午前)", [f"{i}時からは空いてますか？" for i in [8,9,10,11,12]])
    add("時間(昼)", [f"{i}時からは空いてますか？" for i in [11,12,13,14,15,16]])
    add("時間(夕方)", [f"{i}時からは空いてますか？" for i in [14,15,16,17,18,19]])
    add("時間(夜)", [f"{i}時からは空いてますか？" for i in [18,19,20,21,22,23]])
    ## 予約 9
    m = input_data["日付(月)"]
    d = input_data["日付(日)"]
    h = input_data["何時から"]
    add("予約", [f"{m}月{d}日の{h}時に予約をお願いします", f"{m}月{d}日の{h}時に予約をとりたいのですが",
        f"{m}月{d}日の{h}時に予約したいのですけれども",f"{m}月{d}日の{h}時に伺いたいのですが"])
    ## 日付 10
    month = input_data["日付(月)"]
    date = input_data["日付(日)"]
    add("日付", [f"{month}月{date}日の予約は可能ですか",f"{month}月{date}日でお願いします。",f"{month}月{date}日に予約したいです。"])
    ## 記念日 11
    aniversary = input_data["記念日"]
    add("誕生日", [f"{month}月{date}日は{aniversary}です。",f"{date}日は{aniversary}です。",f"{aniversary}をお祝いしたいと思っています。"])
    ## 電話番号 12
    phone = input_data["電話番号"]
    add("電話", [f"電話番号は{phone}なります。",f"電話番号は{phone}です。",f"ケータイは{phone}です。"])
    ## クレジットカード 13
    pay = input_data["支払いカード"]
    add("クレジットカード", [f"{pay}は使えますか？",f"{pay}で支払います。",f"{pay}加盟店ですか？"])
    ## ポイント Go to eat 14
    point = input_data["ポイント"]
    add("ポイント", [f"{point}は使えますか?",f"{point}対象店ですか？",f"{point}は貯まりますか？"])
    ## 席の位置 15
    place = input_data["席の位置"]
    add("席",[f"席は{place}の近くでお願いします。",f"{place}近くに席をお願いします。",f"{place}側にお願いします。"])
    ## アレルギー 16
    hate = input_data["アレルギー"]
    add("アレルギー",[f"{hate}は食べられません。",f"{hate}が入った食べ物は避けてください。",f"{hate}が嫌いです。",f"{hate}はアレルギーです"])



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
    main(debug_mode=True, skip_input=True, tts_skip=False, stt_skip=True) 

   # test_gui_integration()
