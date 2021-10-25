#!/usr/bin/env python
# -*- coding: utf8 -*-
import tkinter as tk
from tkinter.constants import N
from dataclasses import dataclass
from typing import List

@dataclass
class InputForm:
    label: str
    input_type: type

#入力データいれ
class input_data():
    def __init__(self,a,b,c,d,e):
        self.dict={}
        self.dict["name"] = a
        self.dict["number"] = b
        self.dict["children"] = c
        self.dict["ponta"] = d
        self.dict["dugong"] = e
        self.check()
        self.data=self.dict.copy()#dictに無限追加を避ける
        self.reset()#dictに無限追加を避ける

    def reset(self):
        self.dict = {}

    #無効な入力に対しWARNINGを出す
    def check(self):
        name = self.dict["name"]
        number = self.dict["number"]
        children = self.dict["children"]
        ponta = self.dict["ponta"]
        dugong = self.dict["dugong"]
        if int(number)>100 or int(number)<0:
            print("無効な入力です!!")
            self.dict={}
        else:
            print("正しい入力です。")

    def __repr__(self):
        ret = "= input data ="
        ret += "\n".join([f"  {key}: {self.data[key]}" for key in self.data.keys()])
        return ret

    def __call__(self):
        return self.data

class Application(tk.Frame):
    def __init__(self, master, input_form_list: List[InputForm]):
        super().__init__(master)
        self.frame = master
        self.frame.title(u"input")
        self.frame.geometry("1500x750")
        self.data={}

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

        self.create_weget(input_form_list)

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

    def create_weget(self, input_form_list):
        # (参考)
        # for input_form in input_form_list:
        #     if input_form.type is int:
        #         IntVarの処理
        #     elif input_form.type is str:
        #         StringVarの処理

        #氏名
        self.Static1 = tk.Label(text='氏名',font = ("Helvetica", "20"))
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
        data=self.Send_data(event)
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
        ip_data=input_data(value_name,value_num,value_children_num,value_ponta,value_dugong)
        #debug
        print(ip_data)
        #
        self.EditBox1.delete(0,tk.END)
        self.EditBox2.delete(0,tk.END)
        self.EditBox3.delete(0,tk.END)
        self.EditBox4.delete(0,tk.END)
        self.EditBox5.delete(0,tk.END)
        #
        self.data=ip_data()

def main(input_form_list=None):
    if input_form_list is None:
        input_form_list = get_test_input_forms()
    root = tk.Tk()
    app = Application(master=root, input_form_list=input_form_list)
    app.mainloop()
    return app.data

def get_test_input_forms():
    return [InputForm("名前",str), InputForm("コース名",str), InputForm("人数",int), InputForm("子供の人数",int),
            InputForm("狸の匹数",int), InputForm("ジュゴン",int)]

if __name__ == '__main__': # このファイルが直接呼ばれたときだけ以下を呼ぶ
    ret = main()
    print(ret)


