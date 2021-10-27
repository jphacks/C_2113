# -*- coding:utf-8 -*-
import sys
import tkinter as tk
from tkinter import ttk
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

    #root の設定（サイズは1380x900）
    root = tk.Tk()
    root.title(u"main")
    root.geometry("1380x850")
    root.config(background="white")

    global sub_root
    sub_root=None
    global speaking_string
    speaking_string=tk.StringVar(value="デフォルト")
    listening_string=tk.StringVar(value="デフォルト")
        

    #プロダクトタイトル
    frame_title=tk.Frame(
        root,
        background='#00b0d9'
    )
    frame_title.grid(row=0,column=0,columnspan=5,sticky=tk.NSEW)


    string_title = tk.Label(
        frame_title,
        text=u"rityo_math（プロダクト名）",
        foreground="white",
        background='#00b0d9',
        font=("ＭＳ Ｐゴシック", "35", "bold"),
        height=1,
        width=30,
    )
    string_title.pack(anchor=tk.NW,side=tk.TOP,ipady=10,)

    #横線
    canvas = tk.Canvas(
        frame_title,
        height=8,
        bg="#102D63",
    )
    canvas.pack(anchor=tk.N,side=tk.TOP,fill="x")
    
    
    #認識音声/発声音声 出力画面
    frame_view=tk.Frame(
        root,
        bg="white",
    )
    frame_view.grid(row=1,column=0,columnspan=5,pady=10)


    #認識音声側
    frame_listening=tk.LabelFrame(
        frame_view,
        bg="white",
        bd=2,
        relief="solid",
        text="相手の音声",
        font=("Helvetica", "30", "bold"),
        foreground="#3F3D94",
        #foreground="#1E01F4",
        labelanchor=tk.N,
    )
    frame_listening.grid(row=0,column=0,padx=8)

    #相手の発言を表示
    string_listening= tk.Label(
        frame_listening,
        textvariable=listening_string, 
        foreground='#000000', 
        background="#ffffff",
        font=("Helvetica", "25", "bold"),
        height=5,
        width=49,
        # これで改行できるけどどうですか？
        wraplength=680,
    )
    string_listening.pack()

    #自分側
    frame_speaking=tk.LabelFrame(
        frame_view,
        bg="white",
        bd=2,
        relief="solid",
        text="自分の音声",
        font=("Helvetica", "30", "bold"),
        foreground="#3F3D94",
        #foreground="#1E01F4",
        labelanchor=tk.N,
    )
    frame_speaking.grid(row=0,column=1,padx=8)

    #自分の発言を表示
    string_speaking= tk.Label(
        frame_speaking,
        textvariable=speaking_string, 
        foreground='#000000', 
        background="#ffffff",
        font=("Helvetica", "25", "bold"),
        height=5,
        width=49,
        wraplength=680,
    )
    string_speaking.pack()


    #ログのLINE表示用スペース
    frame_LINE=tk.LabelFrame(
        root,
        bg="white",
        bd=1,
        font=("Helvetica", "30", "bold"),
        foreground="#00B900",
        text="会話ログ",
        labelanchor=tk.N,
        relief="solid",
        highlightcolor="blue",
        
    )
    frame_LINE.grid(row=2,column=0,columnspan=2,rowspan=2,padx=8,sticky=tk.NSEW)

    #LINE表示用
    string_LINE= tk.Label(
        frame_LINE,
        text=u" 1 \n 2 \n 3 \n 4 \n 5 \n 6 \n 7 \n 8 \n 9 \n 10 \n 11 \n 12 \n 13 \n 14 \n 15 " , 
        foreground='#000000', 
        background="#ffffff",
        font=("Helvetica", "25", ),
        height=15,          
        width=35
    )

    string_LINE.pack(anchor=tk.N,side=tk.TOP,)


    #ボタンが押されたときの関数
    #発声文章リストを受け取る
    #tts_qのところはデフォルト引数のままでいい

    def speaking_button_popup(list, tts_q=tts_queue):
        def inner_func(tts_q):
        #popup window
            global sub_root
            global speaking_string
            global tts_queue
            if sub_root is None or not sub_root.winfo_exists():
                pass
            else:
                sub_root.destroy()
            sub_root=tk.Toplevel(root)
            sub_root.config(background="white")
            sub_root.title("文章選択")
            sub_root.geometry("800x700")

            #radio button 変数
            v = tk.IntVar(value=0)

            for i in range(len(list)):

                radio = tk.Radiobutton(
                    sub_root,
                    text=list[i],
                    variable=v,
                    value=i,
                    font=("Helvetica", "25", ),
                    foreground="red",
                    background="white"
                )
                radio.pack()

            
            def destroy_func(v, tts_q):
                def inner_destroy(tts_q):
                    global sub_root
                    global speaking_string
                    sub_root.destroy()
                    speak_txt = list[v.get()]
                    tts_q.put(speak_txt)
                    speaking_string.set(speak_txt)

                return lambda:inner_destroy(tts_q)

            sub_final_Button=tk.Button(
                sub_root,
                text="発声する",
                font=("Helvetica", "25", "bold"),
                relief=tk.RAISED,
                pady=5,
                command=destroy_func(v, tts_q)
            )
            sub_final_Button.pack()

        return lambda:inner_func(tts_q)
    


    #選択肢ボタン
    frame_Button=tk.LabelFrame(
        root,
        bg="white",  
        bd=0,
        text="話題",
        foreground="#102D63",
        font=("Helvetica", "30", "bold"),
        labelanchor=tk.N
    )
    frame_Button.grid(row=2,column=2,columnspan=1,sticky=tk.NSEW)

    string_button=tk.Label(
        frame_Button,
        text="関連する候補文章リストを表示します。",
        font=("Helvetica", "20"),
        background="white",
    )
    string_button.grid(row=0,column=0,columnspan=2)


    for i in range(2):
        for j in range(6):
            Button_choice=tk.Button(
                frame_Button,
                text=buttons[6*i+j].label,
                font=("Helvetica", "25"),
                background="white",
                relief=tk.RAISED,
                pady=5,
                command=speaking_button_popup(buttons[6*i+j].choices)
            )
            Button_choice.grid(row=1+j,column=i,sticky=tk.NSEW)      

    

    def speaking_typing_popup():
        #popup window
        global sub_root
        global speaking_string
        if sub_root is None or not sub_root.winfo_exists():
            pass
        else:
            sub_root.destroy()
        sub_root=tk.Toplevel(root)
        sub_root.config(background="white")
        sub_root.title("文章選択")
        sub_root.geometry("800x700")

        typing_title=tk.Label(
        sub_root,
        text=u"話したい文章を記入してください", 
        #foreground='#00b0d9', 
        background='#FFFFFF',
        font=("Helvetica", "30", ),
        height=1,
        width=40
        )
        typing_title.pack()

        temp_v=tk.StringVar(value="")
        typing_box = tk.Entry(
            sub_root,
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
            pady=5,
            command=destroy_typing_func
        )
        sub_final_Button.pack()

        
        

    #選択肢自由記述
    Button_choice_free=tk.Button(
        frame_Button,
        text="自由入力",
        font=("Helvetica", "25", "bold"),
        foreground="indigo",
        background="yellow",
        relief=tk.RAISED,
        pady=5,
        width=25,
        command=speaking_typing_popup
    )
    Button_choice_free.grid(row=7,column=0,columnspan=2,sticky=tk.NSEW)


    #一般的な言葉のボタン
    #赤字は即発声をイメージ

    def speaking_Button_quick(text):
        def inner_speaking_Button_quick():
            speaking_string.set(text)
        return inner_speaking_Button_quick



    frame_general=tk.LabelFrame(
        root,
        bg="white",  
        bd=0,
        text="候補文（即発声）",
        foreground="#102D63",
        font=("Helvetica", "30", "bold"),
        labelanchor=tk.N
    )
    frame_general.grid(row=2,column=3,columnspan=2,sticky=tk.NSEW)


    #ページ遷移用
    global v_general
    v_general = tk.IntVar(value=0)

    def Button_place():
        global v_general
        for i in range(6):
            if v_general.get()==0:
                val_general=buttons[-1].choices[i]
                
            elif v_general.get()==1:
                val_general=buttons[-1].choices[6+i]
            Button_general=tk.Button(
                frame_general,
                text=val_general,
                font=("Helvetica", "25",),
                foreground="red",
                background="#e6f7f6",
                height=1,
                width=35,
                pady=5,
                command=speaking_Button_quick(val_general),
                relief=tk.RAISED,
                
            )
            Button_general.grid(row=i+1,column=0,columnspan=2,sticky=tk.NSEW)
    
    #ボタン初期配置
    Button_place()
    
            
    for i in range(2):
        radio = tk.Radiobutton(
            frame_general,
            text=f"ページ {i+1}",
            variable=v_general,
            value=i,
            font=("Helvetica", "25"),
            background="white",
            command=Button_place
        )
        radio.grid(row=7,column=i)
    

    string_general=tk.Label(
        frame_general,
        text="便利な候補文章を即発声します。",
        font=("Helvetica", "20"),
        background="white",
    )
    string_general.grid(row=0,column=0,columnspan=2)

    frame_tale=tk.Frame(
        root,
        #background='#00b0d9',
        background="white"
    )
    frame_tale.grid(row=3,column=3,columnspan=2,sticky=tk.NSEW)


    string_tale = tk.Label(
        frame_tale,
        text=u"aphacks",
        foreground="white",
        background='#00b0d9',
        font=("ＭＳ Ｐゴシック", "15", "bold"),
        height=1,
        width=15,
    )
    string_tale.pack(anchor=tk.E,side=tk.TOP,ipady=10,)

    

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
    

