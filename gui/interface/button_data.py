# 基底クラス
# ボタンのデータを表す
class Button:
    def __init__(self, label: str, choices: list):
        # label     : ボタンの表示名
        # choices   : 選択肢
        self.label = label
        self.choices = choices
    
    def __repr__(self):         # インスタンスをprintしたときの出力
        return f'[[Button]] label={self.label}, choices={self.choices}'

# 継承クラス
class JikanButtonExample(Button):
    def __init__(self):
        super().__init__("時間", [f'{i}時でお願いします' for i in range(9, 21)])

# 継承クラス
class NinzuuButtonExample(Button):
    def __init__(self):
        super().__init__("人数", [f'{i}人なんですけれどもいけますか' for i in range(1,7)])
    
# 継承クラス
class ExampleButton(Button):
    def __init__(self):
        super().__init__("計数工学",
            ["すべての極が任意に配置できる性質",
                "確率モデルに基づいた、MMSEの意味で最適なオブザーバ",
                "自己相関係数を用いき過去の入力の線型で予測を行うフィルタ",
                "非反転増幅とバンドパスフィルタを組み合わせた発振回路",
                "東京湾にかかる橋"])

if __name__ == '__main__':
    print("まずはクラスのインスタンスを作ります")
    jikan = JikanButtonExample()
    ninzu = NinzuuButtonExample()
    example = ExampleButton()

    print("\n各クラスの内部変数を確認します")
    print(jikan)
    print(ninzu)
    print(example)

    print("\nこれは直接確認することも出来ます。例えば、")
    printv = lambda x:print(f"{x}と書くと、{eval(x)}という値が得られます。")
    printv("jikan.label")
    printv("ninzu.choices")

