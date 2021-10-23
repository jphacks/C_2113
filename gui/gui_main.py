# -*- coding:utf-8 -*-
import sys
import tkinter



root = tkinter.Tk()
root.title(u"main")
root.geometry("400x300")

Static1 = tkinter.Label(text=u'コミュ障最高！', foreground='#00b0d9', background='#FFFFFF')
Static1.pack()

def DeleteStatic1(event):
    Static1.pack_forget() 


Button_1 = tkinter.Button(text=u"はい")
Button_1.bind("<Button-1>",DeleteStatic1)
Button_1.place(x=50,y=100)

Button_2 = tkinter.Button(text=u"結構です")
Button_2.bind("<Button-1>",DeleteStatic1)
Button_2.place(x=50,y=150)

Button_3 = tkinter.Button(text=u"お願いします")
Button_3.bind("<Button-1>",DeleteStatic1)
Button_3.place(x=50,y=200)

Edit_Box=tkinter.Entry(width=25)
Edit_Box.place(x=160,y=200)

root.mainloop()