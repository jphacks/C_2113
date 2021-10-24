#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
import tkinter as tk
from tkinter.constants import N

root = tk.Tk()
root.title(u"input")
root.geometry("1500x750")

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

#データ転送用関数
def Send_data(event):
  value_name = EditBox1.get()
  value_num = EditBox2.get()
  value_children_num = EditBox3.get()
  value_ponta = EditBox4.get()
  value_dugong = EditBox5.get()
  data=input_data(value_name,value_num,value_children_num,value_ponta,value_dugong)
  #debug
  print(data.name)
  print(data.number)
  print(data.dugong)
  #
  EditBox1.delete(0,tk.END)
  EditBox2.delete(0,tk.END)
  EditBox3.delete(0,tk.END)
  EditBox4.delete(0,tk.END)
  EditBox5.delete(0,tk.END)
  #
  return data

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


#氏名
Static1 = tk.Label(text=u'氏名',font = ("Helvetica", "20"))
Static1.pack()
EditBox1 = tk.Entry(width=25)
EditBox1.pack()

#人数
Static2 = tk.Label(text=u'人数',font = ("Helvetica", "20"))
Static2.pack()
EditBox2 = tk.Entry(width=25)
EditBox2.pack()

#うち子供
Static3 = tk.Label(text=u'子供の人数',font = ("Helvetica", "20"))
Static3.pack()
EditBox3 = tk.Entry(width=25)
EditBox3.pack()

#Ponta
Static4 = tk.Label(text=u'Ponta',font = ("Helvetica", "20"))
Static4.pack()
EditBox4 = tk.Entry(width=25)
EditBox4.pack()

#dugong
Static5 = tk.Label(text=u'dugong',font = ("Helvetica", "20"))
Static5.pack()
EditBox5 = tk.Entry(width=25)
EditBox5.pack()


#ボタン
Button = tk.Button(text=u'決定')
Button.bind("<Button-1>",Send_data) 
Button.pack()

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

root.mainloop()