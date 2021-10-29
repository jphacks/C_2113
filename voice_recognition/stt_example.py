import threading
import stt_library
import queue
import sys

if __name__ == "__main__":
	queue_from_stt = queue.Queue()
	stt_thread = threading.Thread(target = stt_library.stt_main, args = (queue_from_stt, ))
	stt_thread.start()
	sys.stdout.flush()
	while True:
		stt_result = queue_from_stt.get()
		if (stt_result.is_final):
			# is_final フラグが立っているとき、音声解析が一通り終わっていることを表す。
			# 次に来るパッケージに現在のパッケージの内容が引き継がれない。
			# log としては is_final フラグが立っているものだけを使えば良い。
			print("[[VOICE RECOGNITION]]", stt_result.alternatives[0].transcript, end = '\n')
		else:
			# is_final フラグが立っていないとき、音声解析が完全には終わってはおらず、暫定の解析結果であることを表す。
			# 「あの子」→「あのこと」みたいに修正され得るので、次にパッケージが来た際には、現在の出力結果を上書きすべき。
			print("[[VOICE RECOGNITION]]", stt_result.alternatives[0].transcript, end = '\r')
