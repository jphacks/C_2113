import base64
import numpy as np

import urllib.request
import json
import subprocess as sp
from playsound import playsound
import queue

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../common'))
from interface_struct import SpeakingData

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
	print(res.stderr)
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


def output_mp3(dat: dict, ofile: str) -> int:
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
	return len(uint8_dat) / 2 / 24  # playing time in ms. 24,000 Hz with 2 bytes


def gtts(txt: str, ofile: str) -> int:

	# Returns playing time in ms.

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
			ret = output_mp3(body, ofile)
			print("done..")
		return ret
	except urllib.error.URLError as e:
		print("error happen...")
		print(e.reason)
		print(e)
		return -1


def tts_and_speak(txt: str, id: int, output_queue: queue.Queue = None) -> None:
	ofile = "tts" + str(id) + ".mp3"
	playtime = gtts(txt, ofile)
	if (output_queue is not None):
		output_queue.put(SpeakingData(txt=txt, sec=playtime))
	playsound(ofile)

def main(txt_queue: queue.Queue, output_queue: queue.Queue, debug: bool = False) -> None:
    print("[[TTS]]", f"debug={debug}")
    i = 0
    while    True:
        try:
            txt = txt_queue.get(timeout=500.0)
            print("[[TTS]]", "get:", txt)
            if debug:
                output_queue.put(SpeakingData(txt=txt, sec=0.1*len(txt)))
                print("[[TTS]]", "speak:", txt)
            else:
                tts_and_speak(txt, i, output_queue)
            i += 1
        except:
            print("[[TTS]]", "get text timeout.")
            continue


