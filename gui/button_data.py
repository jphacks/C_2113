from dataclasses import dataclass
from typing import List

@dataclass
class ButtonData:
    label: str
    choices: List[str]

if __name__ == '__main__':
    ninzu = ButtonData("人数", [f'{i}人でお願いします' for i in range(1,7)])
    jikan = ButtonData("時間", [f'{i}時にお願いします' for i in range(9,21)])

    printB = lambda x:print(f'=={x}==\n{eval(x)}\n')
    printB("ninzu")
    printB("jikan")
