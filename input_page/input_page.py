#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
import tkinter
from tkinter.constants import N

global value_name, value_num

class input_data():
    def __init__(self,s,k):
        self.name = s
        self.number = k

def Send_data(event):
  value_name = EditBox1.get()
  value_num = EditBox2.get()
  data=input_data(value_name,value_num)
  #debug
  print(data.name)
  print(data.number)
  #
  EditBox1.delete(0,tkinter.END)
  EditBox2.delete(0,tkinter.END)
  #
  return data

root = tkinter.Tk()
root.title(u"入力画面")
root.geometry("500x300")

#ラベル
Static1 = tkinter.Label(text=u'氏名')
Static1.pack()
#Entry
EditBox1 = tkinter.Entry(width=25)
EditBox1.pack()

value_name = EditBox1.get()#名前が入る

Static2 = tkinter.Label(text=u'人数')
Static2.pack()
EditBox2 = tkinter.Entry(width=25)
EditBox2.pack()

value_num = EditBox2.get()#人数を入れる

#ボタン
Button = tkinter.Button(text=u'決定')
Button.bind("<Button-1>",Send_data) 
Button.pack()

root.mainloop()