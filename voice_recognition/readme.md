last modified: 29, Oct.

# google speech-to-text api を使ったファイルの説明

google speech-to-text api を使った音声認識コードが置かれています。

**注意:** 無料枠は現状 60 分しか無いので注意すること (近いうちに無限にするつもりなので、必要な分は惜しまず使って欲しいですが by 坂部)

## Requirements

Google tts の動作環境 (tts フォルダ内参照) に加え、更に次のものが必要。

- Python パッケージ (いずれも pip でインストール)
  - google
  - google-cloud
  - google-cloud-speech
  - pyaudio
    
	※ pyaudio のインストール時に、`fatal error: portaudio.h: No such file or directory` と怒られることがある。その場合は `apt install portaudio19-dev` をすれば解決する。

## ファイルの説明

### googles_code.py

google speech-to-text のリアルタイム変換機能を走らせる。実行してマイクに向かって話すと、テキストデータ化されて terminal に表示される。

コードの内容はほぼ [Googleの公式ページ](https://cloud.google.com/speech-to-text/docs/streaming-recognize?hl=ja#speech-streaming-mic-recognize-python) からのコピペ。

### stt_library.py

上記の google_code.py を、queue での通信に対応させたもの。使い方の具体例は stt_example.py を参照すること。特に queue の戻り値の扱いが特殊なので、stt_example.py の中のコメントを読んで欲しい。

【割と重要】multithreading の関係で stt_example.py は Ctrl+C では止まらない。音声認識スレッドを停止させるには、「認識終了」と音声入力すること。
