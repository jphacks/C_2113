# -*- coding:utf-8 -*-
import sys
import tkinter as tk
from dataclasses import dataclass
from typing import Dict, List
from threading import Thread
import time
from queue import Queue, Empty

@dataclass
class ButtonData:
    label: str
    choices: List[str]

@dataclass
class SpeakingData:
    txt: str
    sec: float

def main(tts_queue, buttons, speaking_queue=None, listening_queue=None): 

    #root の設定（サイズは1500x750）
    root = tk.Tk()
    root.title(u"main")
    root.geometry("1500x750")

    global sub_root
    global speaking_string
    speaking_string=tk.StringVar(value="デフォルト")
    listening_string=tk.StringVar(value="デフォルト")
        

    #プロダクトタイトル
    frame_title=tk.Frame(
        root,
    )
    frame_title.grid(row=0,column=0,columnspan=5,sticky=tk.NSEW)

    string_title = tk.Label(
        frame_title,
        text=u"rityo_math（プロダクト名）", 
        foreground='#00b0d9', 
        background='#FFFFFF',
        font=("Helvetica", "50", "bold"),
        height=1,
        width=30
    )
    string_title.pack(anchor=tk.N,side=tk.TOP)


    #認識音声/発声音声 出力画面
    frame_view=tk.Frame(
        root,
    )
    frame_view.grid(row=1,column=0,columnspan=5,sticky=tk.NSEW)


    #認識音声側
    frame_listening=tk.Frame(
        frame_view,
        bg="#edf7f5",
        highlightthickness=3, 
        highlightbackground="gray", 
        highlightcolor="red",
        takefocus=True
    )
    frame_listening.pack(anchor=tk.NW,padx=10,pady=10,side=tk.LEFT)

    # 相手が発声中かを表示。
    # 相手が発声中だけ点灯させたい（todo）
    string_listening_flag= tk.Label(
        frame_listening,
        text=u"発声中", 
        foreground="red", 
        background="#ffffff",
        font=("Helvetica", "25", "bold"),
        height=1,
        width=5,
    )
    string_listening_flag.pack(anchor=tk.NE,side=tk.RIGHT)


    #タイトル
    string_listening_title= tk.Label(
        frame_listening,
        text=u"相手の音声", 
        foreground='#000000', 
        background="#ffffff",
        font=("Helvetica", "25", "bold"),
        height=1,
        width=9,
    )
    string_listening_title.pack(anchor=tk.N,side=tk.TOP,pady=5)

    #相手の発言を表示(todo)
    string_listening= tk.Label(
        frame_listening,
        textvariable=listening_string, 
        foreground='#000000', 
        background="#ffffff",
        font=("Helvetica", "25", "bold"),
        height=4,
        width=40,
    )
    string_listening.pack(anchor=tk.NW,side=tk.LEFT)


    #音声出力側
    frame_speaking=tk.Frame(
        frame_view,

        bg="#edf7f5",
        highlightthickness=3, 
        highlightbackground="gray", 
        highlightcolor="red", 
        takefocus=True
    )
    frame_speaking.pack(anchor=tk.NE,padx=10,pady=10,side=tk.RIGHT)

    #自分が発声中かを表示。
    # 自分が発声中だけ点灯させたい(todo)
    string_speaking_flag= tk.Label(
        frame_speaking,
        text=u"発声中", 
        foreground="red", 
        background="#ffffff",
        font=("Helvetica", "25", "bold"),
        height=1,
        width=5,
    )
    string_speaking_flag.pack(anchor=tk.NE,side=tk.RIGHT)


    #タイトル
    string_speaking_title= tk.Label(
        frame_speaking,
        text=u"自分の音声", 
        foreground='#000000', 
        background="#ffffff",
        font=("Helvetica", "25", "bold"),
        height=1,
        width=9,
    )
    string_speaking_title.pack(anchor=tk.N,side=tk.TOP,pady=5)


    #自分が発言している文章が入る(todo)
    #カラオケみたいにしたい(todo)
    #発言中は背景色も変わるようにしたい(todo)
    string_speaking= tk.Label(
        frame_speaking,
        textvariable=speaking_string, 
        foreground='#000000', 
        background="#ffffff",
        font=("Helvetica", "25", "bold"),
        height=4,
        width=40,
        
    )
    string_speaking.pack(anchor=tk.NW,side=tk.LEFT)



    #ログのLINE表示用スペース

    frame_LINE=tk.Frame(
        root,
        bg="#eef7ed",
    )
    frame_LINE.grid(row=2,column=0,columnspan=2,rowspan=3,sticky=tk.NSEW)

    #LINE表示用
    string_LINE= tk.Label(
        frame_LINE,
        text=u"（ここにLINEが入る） 1 \n 2 \n 3 \n 4 \n 5 \n 6 \n 7 \n 8 \n 9 \n 10 \n 11 \n 12 \n 13 \n 14 \n 15", 
        foreground='#000000', 
        background="#ffffff",
        font=("Helvetica", "25", "bold"),
        height=15,          
        width=30
    )

    string_LINE.pack(anchor=tk.N,side=tk.TOP,)



    #ボタンが押されたときの関数
    #発声文章リストを受け取る
    #tts_qのところはデフォルト引数のままでいい
    def speaking_button_popup(dict, tts_q=tts_queue):
        def inner_func(tts_q):
        #popup window
            global sub_root
            global speaking_string
            global tts_queue
            sub_root=tk.Toplevel(root)
            sub_root.title("文章選択")
            sub_root.geometry("750x500")

            #radio button 変数
            v = tk.IntVar(value=0)

            radio_0 = tk.Radiobutton(
                sub_root,
                text=dict[0],
                variable=v,
                value=0,
                font=("Helvetica", "25", "bold"),
            )
            radio_0.pack()

            radio_1 = tk.Radiobutton(
                sub_root,
                text=dict[1],
                variable=v,
                value=1,
                font=("Helvetica", "25", "bold"),
            )
            radio_1.pack()            

            radio_2 = tk.Radiobutton(
                sub_root,
                text=dict[2],
                variable=v,
                value=2,
                font=("Helvetica", "25", "bold"),
            )
            radio_2.pack()
            
            def destroy_func(v, tts_q):
                def inner_destroy(tts_q):
                    global sub_root
                    global speaking_string
                    sub_root.destroy()
                    speak_txt = dict[v.get()]
                    tts_q.put(speak_txt)
                    speaking_string.set(speak_txt)

                return lambda:inner_destroy(tts_q)

            sub_final_Button=tk.Button(
                sub_root,
                text="発声する",
                font=("Helvetica", "25", "bold"),
                relief=tk.RAISED,
                foreground="red",
                pady=5,
                command=destroy_func(v, tts_q)
            )
            sub_final_Button.pack()

        return lambda:inner_func(tts_q)



    #選択肢ボタン
    frame_Button=tk.Frame(
        root,
        bg="#fdf7ff",   
    )
    frame_Button.grid(row=2,column=2,sticky=tk.NSEW)

    string_Button_title=tk.Label(
        frame_Button,
        text=u"話題", 
        foreground='#00b0d9', 
        background='#FFFFFF',
        font=("Helvetica", "30", "bold"),
    )
    string_Button_title.grid(row=0,column=0,sticky=tk.N)



        

    #選択肢(1,1)
    dict_11={0:"サンプル文章０",1:"サンプル文章１",2:"サンプル文章２"}
    Button_choice_11=tk.Button(
        frame_Button,
        text="人数",
        font=("Helvetica", "25", "bold"),
        relief=tk.RAISED,
        pady=5,
        command=speaking_button_popup(dict_11)
    )
    Button_choice_11.grid(row=1,column=0,sticky=tk.NSEW)


    dict_21={0:"サンプル文章０",1:"サンプル文章１",2:"サンプル文章２"}
    #選択肢(2,1)
    Button_choice_21=tk.Button(
        frame_Button,
        text="時間",
        font=("Helvetica", "25", "bold"),
        relief=tk.RAISED,
        pady=5,
        command=speaking_button_popup(dict_21)
    )
    Button_choice_21.grid(row=2,column=0,sticky=tk.NSEW)

    #選択肢(3,1)
    Button_choice_31=tk.Button(
        frame_Button,
        text="キャンセル",
        font=("Helvetica", "25", "bold"),
        relief=tk.RAISED,
        pady=5
    )
    Button_choice_31.grid(row=3,column=0,sticky=tk.NSEW)

    #選択肢(4,1)
    Button_choice_41=tk.Button(
        frame_Button,
        text="選択肢４１",
        font=("Helvetica", "25", "bold"),
        relief=tk.RAISED,
        pady=5
    )
    Button_choice_41.grid(row=4,column=0,sticky=tk.NSEW)

    #選択肢(5,1)
    Button_choice_51=tk.Button(
        frame_Button,
        text="選択肢５１",
        font=("Helvetica", "25", "bold"),
        relief=tk.RAISED,
        pady=5
    )
    Button_choice_51.grid(row=5,column=0,sticky=tk.NSEW)

    #選択肢(6,1)
    Button_choice_61=tk.Button(
        frame_Button,
        text="選択肢６１",
        font=("Helvetica", "25", "bold"),
        relief=tk.RAISED,
        pady=5
    )
    Button_choice_61.grid(row=6,column=0,sticky=tk.NSEW)


    #選択肢(1,2)
    Button_choice_12=tk.Button(
        frame_Button,
        text="選択肢１２",
        font=("Helvetica", "25", "bold"),
        relief=tk.RAISED,
        pady=5
    )
    Button_choice_12.grid(row=1,column=1,sticky=tk.NSEW)

    #選択肢(2,2)
    Button_choice_22=tk.Button(
        frame_Button,
        text="選択肢２２",
        font=("Helvetica", "25", "bold"),
        relief=tk.RAISED,
        pady=5
    )
    Button_choice_22.grid(row=2,column=1,sticky=tk.NSEW)

    #選択肢(3,2)
    Button_choice_32=tk.Button(
        frame_Button,
        text="選択肢３２",
        font=("Helvetica", "25", "bold"),
        relief=tk.RAISED,
        pady=5
    )
    Button_choice_32.grid(row=3,column=1,sticky=tk.NSEW)

    #選択肢(4,2)
    Button_choice_42=tk.Button(
        frame_Button,
        text="選択肢４２",
        font=("Helvetica", "25", "bold"),
        relief=tk.RAISED,
        pady=5
    )
    Button_choice_42.grid(row=4,column=1,sticky=tk.NSEW)

    #選択肢(5,2)
    Button_choice_52=tk.Button(
        frame_Button,
        text="選択肢５２",
        font=("Helvetica", "25", "bold"),
        relief=tk.RAISED,
        pady=5
    )
    Button_choice_52.grid(row=5,column=1,sticky=tk.NSEW)

    #選択肢(6,2)
    Button_choice_62=tk.Button(
        frame_Button,
        text="選択肢６２",
        font=("Helvetica", "25", "bold"),
        relief=tk.RAISED,
        pady=5
    )
    Button_choice_62.grid(row=6,column=1,sticky=tk.NSEW)


    #選択肢(1,3)（ここらはカスタムでできないかな？）
    Button_choice_13=tk.Button(
        frame_Button,
        text="カスタム１",
        font=("Helvetica", "25", "bold"),
        relief=tk.RAISED,
        pady=5
    )
    Button_choice_13.grid(row=1,column=2,sticky=tk.NSEW)

    #選択肢(2,3)（ここらはカスタムでできないかな？）
    Button_choice_23=tk.Button(
        frame_Button,
        text="カスタム２",
        font=("Helvetica", "25", "bold"),
        relief=tk.RAISED,
        pady=5
    )
    Button_choice_23.grid(row=2,column=2,sticky=tk.NSEW)

    #選択肢(3,3)（ここらはカスタムでできないかな？）
    Button_choice_33=tk.Button(
        frame_Button,
        text="カスタム３",
        font=("Helvetica", "25", "bold"),
        relief=tk.RAISED,
        pady=5
    )
    Button_choice_33.grid(row=3,column=2,sticky=tk.NSEW)

    #選択肢(4,3)（ここらはカスタムでできないかな？）
    Button_choice_43=tk.Button(
        frame_Button,
        text="カスタム４",
        font=("Helvetica", "25", "bold"),
        relief=tk.RAISED,
        pady=5
    )
    Button_choice_43.grid(row=4,column=2,sticky=tk.NSEW)

    #選択肢(5,3)（ここらはカスタムでできないかな？）
    Button_choice_53=tk.Button(
        frame_Button,
        text="カスタム５",
        font=("Helvetica", "25", "bold"),
        relief=tk.RAISED,
        pady=5
    )
    Button_choice_53.grid(row=5,column=2,sticky=tk.NSEW)

    #選択肢(6,3)（ここらはカスタムでできないかな？）
    Button_choice_63=tk.Button(
        frame_Button,
        text="カスタム６",
        font=("Helvetica", "25", "bold"),
        relief=tk.RAISED,
        pady=5
    )
    Button_choice_63.grid(row=6,column=2,sticky=tk.NSEW)


    def speaking_typing_popup():
        #popup window
        global sub_root
        global speaking_string
        sub_root=tk.Toplevel(root)
        sub_root.title("文章選択")
        sub_root.geometry("750x500")

        typing_title=tk.Label(
        sub_root,
        text=u"話したい文章を記入してください", 
        foreground='#00b0d9', 
        background='#FFFFFF',
        font=("Helvetica", "30", "bold"),
        height=1,
        width=40
        )
        typing_title.pack()

        temp_v=tk.StringVar(value="")
        typing_box = tk.Entry(
            sub_root,
            #textvariable=speaking_string,
            textvariable=temp_v,
            width=40,
            font=("Helvetica", "30", "bold"),
            
        )
        typing_box.pack()

        
        def destroy_typing_func():
            
            global sub_root
            global speaking_string
            nonlocal temp_v
            sub_root.destroy()
            speaking_string.set(temp_v.get())
            
        

        sub_final_Button=tk.Button(
            sub_root,
            text="発声する",
            font=("Helvetica", "25", "bold"),
            relief=tk.RAISED,
            foreground="red",
            pady=5,
            command=destroy_typing_func
        )
        sub_final_Button.pack()

        
        

    #選択肢自由記述
    Button_choice_free=tk.Button(
        frame_Button,
        text="自由入力",
        font=("Helvetica", "25", "bold"),
        foreground="green",
        relief=tk.RAISED,
        pady=5,
        command=speaking_typing_popup
    )
    Button_choice_free.grid(row=7,column=0,columnspan=3,sticky=tk.NSEW)


    #一般的な言葉のボタン
    #赤字は即発声をイメージ

    def speaking_Button_quick(text):
        def inner_speaking_Button_quick():
            speaking_string.set(text)
        return inner_speaking_Button_quick

    frame_general=tk.Frame(
        root,
        #width=500,
        #height=300,
        bg="#f8faf2",   
    )
    frame_general.grid(row=2,column=3,columnspan=2,sticky=tk.NSEW)


    string_general_title=tk.Label(
        frame_general,
        text=u"general", 
        foreground='#00b0d9', 
        background='#FFFFFF',
        font=("Helvetica", "30", "bold"),
        height=1,
        width=9
    )
    string_general_title.pack(anchor=tk.N)



    Button_general_1=tk.Button(
        frame_general,
        text="よろしくお願いします",
        font=("Helvetica", "25", "bold"),
        foreground="red",
        background="#e6f7f6",
        height=1,
        width=35,
        pady=5,
        relief=tk.RAISED,
        command=speaking_Button_quick("よろしくお願いします")
    )

    Button_general_1.pack(anchor=tk.N)

    Button_general_2=tk.Button(
        frame_general,
        text="そうです",
        font=("Helvetica", "25", "bold"),
        foreground="red",
        height=1,
        width=35,
        pady=5,
        relief=tk.RAISED
    )

    Button_general_2.pack(anchor=tk.N)

    Button_general_3=tk.Button(
        frame_general,
        text="はい",
        font=("Helvetica", "25", "bold"),
        foreground="red",
        height=1,
        width=35,
        pady=5,
        relief=tk.RAISED
    )

    Button_general_3.pack(anchor=tk.N)

    Button_general_4=tk.Button(
        frame_general,
        text="結構です",
        font=("Helvetica", "25", "bold"),
        foreground="red",
        height=1,
        width=35,
        pady=5,
        relief=tk.RAISED
    )

    Button_general_4.pack(anchor=tk.N)

    Button_general_5=tk.Button(
        frame_general,
        text="少々お待ちください",
        font=("Helvetica", "25", "bold"),
        foreground="red",
        height=1,
        width=35,
        pady=5,
        relief=tk.RAISED
    )

    Button_general_5.pack(anchor=tk.N)

    Button_general_6=tk.Button(
        frame_general,
        text="は？おい俺は計数工学科やぞ",
        font=("Helvetica", "25", "bold"),
        foreground="red",
        height=1,
        width=35,
        pady=5,
        relief=tk.RAISED
    )

    Button_general_6.pack(anchor=tk.N)

    Button_general_7=tk.Button(
        frame_general,
        text="その他",
        font=("Helvetica", "25", "bold"),
        height=1,
        width=35,
        pady=5,
        relief=tk.RAISED
    )

    Button_general_7.pack(anchor=tk.N)


    #説明書き用フレーム
    frame_explain=tk.Frame(
        root,
        #width=500,
        #height=300,
        bg="#f8faf2",   
    )
    frame_explain.grid(row=4,column=2,columnspan=2,sticky=tk.NSEW)

    string_explain = tk.Label(
        frame_explain,
        text=u"rityo_math最高！（説明書き等）", 
        foreground='#00b0d9', 
        background='#FFFFFF',
        font=("Helvetica", "25", "bold"),
        height=1,
        width=30
    )
    string_explain.pack(anchor=tk.N,side=tk.TOP)

    if speaking_queue is not None:
        # Queueを介して喋る内容を受け取る
        def speaking_watcher(q):
            while True:
                try:
                    # [str, float[sec]]
                    data = q.get(timeout=100.0)
                    txt= data.txt
                    speak_time = data.sec
                    n = len(txt)
                    for i in range(1, n+1):
                        speaking_string.set(txt[:i])
                        time.sleep(speak_time / n)
                except Empty:
                    continue

        speaking_thread = Thread(target=lambda:speaking_watcher(speaking_queue))
        speaking_thread.start()

    if listening_queue is not None:
        # Queueを介して認識内容を受け取る
        def listening_watcher(q):
            while True:
                try:
                    txt = q.get(timeout=100.0)
                    n = len(txt)
                    for i in range(1, n+1):
                        listening_string.set(txt[:i])
                        time.sleep(1.0 / n)
                except Empty:
                    continue

        listening_thread = Thread(target=lambda:listening_watcher(listening_queue))
        listening_thread.start()

    return root


if __name__ == '__main__': # このファイルが直接呼ばれたときだけ以下を呼ぶ
    buttons = []
    for i in range(18):
        buttons.append(ButtonData("人数", [f'{i}人でお願いします' for i in range(18)]))

        
    tts_que = Queue()
    def tts_mock(q):
        while True:
            if q.empty():
                time.sleep(0.1)
                continue
            txt = q.get()
            print(f'[[TTS]] {txt}')
    tts_thread = Thread(target=lambda:tts_mock(tts_que))
    tts_thread.start()

    root = main(tts_que, buttons)
    root.mainloop()
    

