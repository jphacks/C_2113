# tts フォルダ内の説明

(Last modified: Oct, 25)

Google tts を使って、Text-To-Speech (テキストデータを音声データに変換する) をするコードが入っています。

Requirements:

- python package
  - numpy
  - playsound
  - subprocess
  - json
  - base64
  - urllib
- Google Cloud Platform のアカウントと、その鍵ファイル

Files

- api.py
  
  text.txt に書かれた文章を tts し、発音します。
  音声ファイルは result2.mp3 に保存されます。

- ttsthread.py

  tts から発声までをまとめて行う関数が実装されています。また、発声開始のタイミングで、所要時間 [ms] を queue に書き込みます。

  使用例が ttsthread_example.py にあります。
  - tts_and_speak(txt, id)

    tts から発声までをまとめて行う関数。
    - txt: 発音して欲しい日本語の文章
    - id: 出力ファイルの id。例えば id=7 であれば、tts7.mp3 というファイルに音声が保存される。
    - output_queue: 言うのにかかる時間を output する queue。
