from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

# GUI用パッケージtkinterを読み込みます。
from tkinter import *

bot = ChatBot("チャットボット試作版")
training_ = open('chat.txt', 'r').readlines()
training2_ = open('chat2.txt', 'r').readlines()

trainer = ListTrainer(bot)
trainer.train(training_)
trainer.train(training2_)

'''
ここからTkinterでGUI画面の要素を定義していきます。
まず、GUI画面の土台を定義します。この後、画面上の各パーツを定義してセットすることを繰り返します。
'''
root = Tk()

# 画面のサイズを定義
root.geometry("600x400")

# 画面のタイトルを定義
root.title("チャットボット試作版")

# フレーム(画面上の各パーツを配置するための枠)を定義
frame = Frame(root)


# スクロールバーを定義
sc = Scrollbar(frame)
# スクロールバーをセット
sc.pack(side=RIGHT, fill=Y)


# リストボックスを定義
msgs = Listbox(frame, width=80, height=20, yscrollcommand=sc.set)
# リストボックスをセット
msgs.pack(side=LEFT, fill=BOTH, pady=10)

#フレームをセット
frame.pack()


# テキストボックスを定義
textF = Entry(root, font=("Courier", 10),width=50)
# テキストボックスをセット
textF.pack()


# ボタンを押したときの動きについて関数を定義
def ask_from_bot():
    query = textF.get()
    answer_from_bot = bot.get_response(query)
    msgs.insert(END, "you : " + query)
    msgs.insert(END, "bot : " + str(answer_from_bot))
    textF.delete(0, END)
    msgs.yview(END)

# ボタンを定義
btn = Button(root, text="質問をどうぞ", font=("Courier", 10),bg='white', command=ask_from_bot)
# ボタンをセット
btn.pack()

# この関数を呼ぶとボタンを押す動きになる。
def enter_function(event):
    btn.invoke()

# エンターキーを押すとenter_functionを呼ぶ（つまり、エンターキーを押すとボタンを押すのと同じ動きになる。）
root.bind('<Return>', enter_function)


# TkinterでGUI画面を起動する。
root.mainloop()