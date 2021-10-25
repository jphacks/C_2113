import ttsthread
import threading
import sys

if __name__ == "__main__":
	i = 0
	while (True):
		txt = sys.stdin.readline()[:-1]
		thread = threading.Thread(target=ttsthread.tts_and_speak, args=(txt, i))
		i += 1
		thread.start()

