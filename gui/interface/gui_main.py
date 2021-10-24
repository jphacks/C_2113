import ButtonData


def main(say, buttons) # 名前は自由に変えてもらって大丈夫です
    pass # ここに処理を書く


if __name__ == '__main__': # このファイルが他のファイルから直接呼ばれたときだけ以下を呼ぶ
    # 18個のボタンを作る
    buttons = [ButtonData.JikanButtonExample()]
    buttons += [ButtonData.NinzuuButtonExample()]
    buttons += [ButtonData.ExampleButton() for i in range(16)]
        
    # mainを呼ぶ
    main(lambda x:f'[[say]] {x}', buttons)

