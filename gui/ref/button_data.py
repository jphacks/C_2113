# 基底クラス
# ボタンのデータを表す
class Button:
    def __init__(self, label: str, choices: list):
        # label     : ボタンの表示名
        # choices   : 選択肢
        self.label = label
        self.choices = choices
    
    def say(self, txt):
        print(f'[[Button]] {txt}')

    def __call__(self, choice): # インスタンスに()を付けて呼び出す
        # フォーマットしてsayを呼び出す
        self.say(choice)

    def __repr__(self):         # インスタンスをprintしたときの出力
        return f'[[Button]] label={self.label}, choices={self.choices}'

# 継承クラス
class JikanButtonExample(Button):
    def __init__(self):
        super().__init__("時間", [f'{i}時' for i in range(9, 21)])

    def __call__(self, choice):
        self.say(f'{choice}時でお願いします')

# 継承クラス
class NinzuuButtonExample(Button):
    def __init__(self):
        super().__init__("人数", [f'{i}人' for i in range(1,7)])
        
    def __call__(self, choice):
        self.say(f'{choice}人でお願いします')
    
    def say(self, txt): # override
        print(f'[[人数]] (大きな声で) {txt}')

if __name__ == '__main__':
    print("まずはクラスのインスタンスを作ります")
    jikan = JikanButtonExample()
    ninzu = NinzuuButtonExample()

    print("\n各クラスの内部変数を確認します")
    print(jikan)
    print(ninzu)


    print("\n2人を11時からでお願いしてみましょう")
    jikan(11)
    ninzu(2)

