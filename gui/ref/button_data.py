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

# 継承クラス
class ExampleButton(Button):
    def __init__(self):
        self.dic = {
            "可制御性":"すべての極が任意に配置できる性質",
            "カルマンフィルタ":"確率モデルに基づいた、MMSEの意味で最適なオブザーバ",
            "線型予測フィルタ":"自己相関係数を用いき過去の入力の線型で予測を行うフィルタ",
            "ウィーンブリッジ発振回路":"非反転増幅とバンドパスフィルタを組み合わせた発振回路",
            "レインボーブリッジ":"東京湾にかかる橋"
        }
        super().__init__("行列", list(self.dic.keys()))

    def __call__(self, choice):
        if choice in self.dic:
            self.say(self.dic[choice]+"でお願いします")

if __name__ == '__main__':
    print("まずはクラスのインスタンスを作ります")
    jikan = JikanButtonExample()
    ninzu = NinzuuButtonExample()
    example = ExampleButton()

    print("\n各クラスの内部変数を確認します")
    print(jikan)
    print(ninzu)
    print(example)

    print("\n11時から2人カルマンフィルタでお願いしてみましょう")
    jikan(11)
    ninzu(2)
    example("カルマンフィルタ")


