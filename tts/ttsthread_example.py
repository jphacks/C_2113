import ttsthread
import threading
import sys
import queue

if __name__ == "__main__":
	i = 0
	times_in_ms = queue.Queue()
	while (i < 3):
		txt = sys.stdin.readline()[:-1]
		thread = threading.Thread(target=ttsthread.tts_and_speak, args=(txt, i, times_in_ms))
		i += 1
		thread.start()
	while (not times_in_ms.empty()):
		print(times_in_ms.get())
