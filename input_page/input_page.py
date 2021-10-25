#!/usr/bin/env python
# -*- coding: utf8 -*-
import tkinter as tk
from tkinter.constants import N
from dataclasses import dataclass
from typing import List

@dataclass
class InputForm:
    label: str
    input_type: type    # int,strの値を取る

#入力データいれ
class input_data():
    def __init__(self,value_dict):
        self.dict=value_dict
        #self.check()
        self.data=self.dict.copy()#dictに無限追加を避ける
        self.reset()#dictに無限追加を避ける

    def reset(self):
        self.dict = {}

    #無効な入力に対しWARNINGを出す
    '''
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
    '''

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
        self.EditBox_dict={}

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
        
        
        for input_form in input_form_list:
            if input_form.input_type is int:
                Static = tk.Label(text=input_form.label,font = ("Helvetica", "20"))
                Static.pack()
                EditBox = tk.Entry(width=25,textvariable=tk.IntVar())
                EditBox.pack()
                self.EditBox_dict[input_form.label]=EditBox
                
            elif input_form.input_type is str:
                Static = tk.Label(text=input_form.label,font = ("Helvetica", "20"))
                Static.pack()
                EditBox = tk.Entry(width=25,textvariable=tk.StringVar())
                EditBox.pack()
                self.EditBox_dict[input_form.label]=EditBox
                
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
        value_dict={}
        for key in self.EditBox_dict:
            value = self.EditBox_dict[key].get()
            value_dict[key]=value
        ip_data=input_data(value_dict)
        #debug
        print(ip_data)
        #
        for key in self.EditBox_dict:
            self.EditBox_dict[key].delete(0,tk.END)
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


