import base64
import numpy as np

import urllib.request
import json
import subprocess as sp
from playsound import playsound

# copy from https://qiita.com/to_obara/items/d8d5c92c2ea85a197e2d


def get_token() -> str:
	"""
    Google Text-To-Speechの認証した上で、gcloudをセットアップした状態で
    tokenを取得するために、gcloud auth print-access-tokenの結果を取得する
    """
	res = sp.run('gcloud auth application-default print-access-token',
	             shell=True,
	             stdout=sp.PIPE,
	             stderr=sp.PIPE,
	             encoding='utf-8')
	print("[[TTS]]", res.stderr)
	return res.stdout.strip()


def makeRequestDict(txt: str) -> dict:
	"""
    Google Text-To-Speechへリクエストのための情報を生成する
    SSMLには未対応

    Args:
        txt(in): 音声合成するテキスト

    Returns:
        音声合成するために必要な情報をdictで返却する
    """
	dat = {
	    "audioConfig": {
	        "audioEncoding": "LINEAR16",
	        "pitch": 0,
	        "speakingRate": 1
	    },
	    "voice": {
	        "languageCode": "ja-JP",
	        "name": "ja-JP-Standard-B"
	    }
	}

	dat["input"] = {"text": txt}
	return dat


def output_mp3(dat: dict, ofile: str) -> None:
	"""
    Google Text-To-Speechへリクエストした結果を元に音声データにしてファイルに書き込む

    Args:
        dat(in):   リクエストした結果得られたJSON文字列をdictにしたもの
        ofile(in): 音声データを書き出すファイル名
    """
	b64str = dat["audioContent"]
	binary = base64.b64decode(b64str)
	uint8_dat = np.frombuffer(binary, dtype=np.uint8)
	with open(ofile, "wb") as f:
		f.write(uint8_dat)


def gtts(txt: str, ofile: str) -> None:

	dat = makeRequestDict(txt)
	req_data = json.dumps(dat).encode()

	url = 'https://texttospeech.googleapis.com/v1/text:synthesize'
	token = get_token()
	req_header = {
	    'Authorization': f"Bearer {token}",
	    'Content-Type': 'application/json; charset=utf-8',
	}
	req = urllib.request.Request(url,
	                             data=req_data,
	                             method='POST',
	                             headers=req_header)

	try:
		with urllib.request.urlopen(req) as response:
			dat = response.read()
			body = json.loads(dat)
			output_mp3(body, ofile)
			print("[[TTS]]""done..")
	except urllib.error.URLError as e:
		print("[[TTS]]""error happen...")
		print("[[TTS]]", e.reason)
		print("[[TTS]]", e)


if __name__ == "__main__":
	with open("text.txt", "r") as fin:
		txt = fin.read()
	txt = txt[:-1]
	gtts(txt, "result2.mp3")
	playsound("result2.mp3")
