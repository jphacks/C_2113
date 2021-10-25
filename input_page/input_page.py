#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
import tkinter as tk
from tkinter.constants import N


#入力データいれ
class input_data():
    def __init__(self,a,b,c,d,e):
        self.name = a
        self.number = b
        self.children = c
        self.ponta = d
        self.dugong = e
        self.check()

    #無効な入力を弾く(ただデモではいらないなと思ったので後で)
    def check(self):
        name = self.name
        number = self.number
        children = self.children
        ponta = self.ponta
        dugong = self.dugong
        if int(number)>100 or int(number)<0:
            print("無効な入力です!!")
        else:
            print("正しい入力です。")

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.frame = master
        self.frame.title(u"input")
        self.frame.geometry("1500x750")
        #タイトル(mainと同一にする)
        string_title = tk.Label(
            text=u"rityo_math（プロダクト名）", 
            foreground='#00b0d9', 
            background='#FFFFFF',
            font=("Helvetica", "50", "bold"),
            height=1,
            width=30
        )
        string_title.pack(anchor=tk.N,side=tk.TOP)

        #説明文
        string_directions = tk.Label(
            text=u"必要事項を記入後、<決定>ボタンを押してください。",
            font=("Helvetica", "30", "bold"),
            bg="#edf7f5",
            highlightthickness=3, 
            highlightcolor="red",
            takefocus=True
        )
        string_directions.pack(anchor=tk.N,side=tk.TOP)

        self.create_weget()

        #オマケ
        string_explain = tk.Label(
            text=u"Have a good reservation!!", 
            foreground='#00b0d9', 
            background='#FFFFFF',
            font=("Helvetica", "30", "bold"),
            height=1,
            width=30
        )
        string_explain.pack(anchor=tk.N,side=tk.BOTTOM)

    def create_weget(self):
        # ウィジェット変数を生成
        #self.sv = tk.StringVar()
        #self.sv.set("")

        #氏名
        self.Static1 = tk.Label(text=u'氏名',font = ("Helvetica", "20"))
        self.Static1.pack()
        self.EditBox1 = tk.Entry(width=25,textvariable=tk.StringVar())
        self.EditBox1.pack()

        #人数
        self.Static2 = tk.Label(text=u'人数',font = ("Helvetica", "20"))
        self.Static2.pack()
        self.EditBox2 = tk.Entry(width=25,textvariable=tk.IntVar())
        self.EditBox2.pack()

        #うち子供
        self.Static3 = tk.Label(text=u'子供の人数',font = ("Helvetica", "20"))
        self.Static3.pack()
        self.EditBox3 = tk.Entry(width=25,textvariable=tk.IntVar())
        self.EditBox3.pack()

        #Ponta
        self.Static4 = tk.Label(text=u'Ponta',font = ("Helvetica", "20"))
        self.Static4.pack()
        self.EditBox4 = tk.Entry(width=25,textvariable=tk.IntVar())
        self.EditBox4.pack()

        #dugong
        self.Static5 = tk.Label(text=u'dugong',font = ("Helvetica", "20"))
        self.Static5.pack()
        self.EditBox5 = tk.Entry(width=25,textvariable=tk.IntVar())
        self.EditBox5.pack()

        #ボタン
        self.Button = tk.Button(text=u'決定')
        self.Button.bind("<Button-1>",self.decision) 
        self.Button.pack()



    def decision(self,event):
        self.Send_data(event)
        self.close_window(event)

    #window閉じる関数
    def close_window(self,event):
        self.frame.destroy()

    #データ転送用関数
    def Send_data(self,event):
        value_name = self.EditBox1.get()
        value_num = self.EditBox2.get()
        value_children_num = self.EditBox3.get()
        value_ponta = self.EditBox4.get()
        value_dugong = self.EditBox5.get()
        data=input_data(value_name,value_num,value_children_num,value_ponta,value_dugong)
        #debug
        print(data.name)
        print(data.number)
        print(data.dugong)
        #
        self.EditBox1.delete(0,tk.END)
        self.EditBox2.delete(0,tk.END)
        self.EditBox3.delete(0,tk.END)
        self.EditBox4.delete(0,tk.END)
        self.EditBox5.delete(0,tk.END)
        #
        return data

#リターンで値を返せば良い
#決定ボタンで閉じるように#まあdone
#実行タイミングを制御できるように

# 適当に継承する
# import ButtonData
def main():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()


if __name__ == '__main__': # このファイルが他のファイルから直接呼ばれたときだけ以下を呼ぶ
    # mainを呼ぶ
    main()