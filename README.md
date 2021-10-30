# **チャットアポ**
## 紹介動画
[![リンク](https://github.com/jphacks/C_2113/blob/master/thumbnail.png?raw=true)](//www.youtube.com/watch?v=2Gr4OAlKFLk)

## 製品概要
**チャットアポ** は飲食店への電話予約を補助するサービスです。さまざまな要因により電話予約を困難だと感じている方を対象に、音声認識・音声合成 技術を用いて円滑な予約をサポートします。

### 背景(製品開発のきっかけ、課題等）
デジタル化社会の進展に伴い、飲食店の web 予約システムが広く普及してきました。一方で、導入コスト等の問題により依然として電話予約しか受け付けないお店が約 32％ もあります。聴覚や発声にハンディキャップがある方、精神的な面で電話に抵抗を感じる方などにとっては、電話予約が大きなハードルとなり、どれだけ行きたいお店であっても我慢せざるを得ない状況にあります。飲食店にとっても、店内であれば顧客に合わせたサポートを直接提供できるものの、顧客の「予約のサポート」の提供は現段階では困難です。
総務省が、手話を用いる仲介者が間に入る聴覚障がい者向け電話サポート (電話リレーサービス https://nftrs.or.jp/ ) を令和３年７月に開始しましたが、上記のような電話予約へ抵抗を感じる全ての層に対する支援とは言えず、運用コストも課題となります。仲介者が入らない電話支援サービスは現在存在していません。

### 製品説明（具体的な製品の説明）
![IMAGE ALT TEXT HERE](https://i.gyazo.com/5c72c4c064209e512513946bda3228ab.png)

## 製品概要
### 特長
#### 1.  チャット感覚で電話予約が可能！
相手の音声が音声認識により文章化され画面に表示されます。手元に用意されたデフォルト文章や自由入力文章を選択する GUI 操作により自分の伝えたい文章を機械音声で発声することができます。

#### 2. 聴覚障がい者向けの UI！
自分が選択した文章のうち、「今なにを」発声しているかを確認できるよう、発声中の文章をリアルタイムで表示します。

#### 3. 会話ログの表示！
チャットアプリ感覚で互いの発声した文章を確認できるため、会話の流れを確認しながら焦ることなく発声文章を選択できます。また、全ての会話ログは通話終了後にテキストファイルとして出力されます。

#### 4. ラグの少ない会話！
より品質の高い機械音声をよりラグがなく高速で発声できる工夫を施しています。また、頻繁に発声する文章を即発声するボタンを配置することで、操作速度のボトルネックへの対策も施しています。

### 解決出来ること
1. 電話予約を困難だと感じている方は、 web 予約とほぼ同等の感覚で電話予約ができ、行きたいお店へ行けるようになる。
1. 飲食店は、新たな顧客を獲得できる。

### 今後の展望
#### 1. サービスの展望
現段階では飲食店のみの予約ですが、今後はより適用範囲を拡大し、より幅広い電話サポートを行います。また、予約内容を記録するカレンダー連携機能の実装も行います。さらに、実際にハンディキャップのある方への聞き込み等も行い、新たな機能の実装の検討も行います。

#### 2. 技術の展望
飲食店側が発声した音声を文字起こしすると同時に手話に翻訳し画面上に表示する機能を実装します。これにより文章よりも手話に親和性がある方も使いやすい UI を目指します。

## 開発技術
### 活用した技術
#### API
* 音声合成: Google Text-to-Speech API
* 音声認識: Google Speech-to-Text のストリーミング認識 API

#### 言語・ライブラリ
* 言語: Python
* GUIウィンドウ作成: tkinter

#### 動作環境・デバイス
* ノートパソコン (Ubuntu)
* スマートフォン (iPhone など)
* スマートフォンとノートパソコン間を Bluetooth 接続。電話の音声ストリームを直接パソコンに転送することで、音声認識の精度を向上。

### 実装した機能
* 電話音声を認識してテキスト化する機能を実装。
* テキストを音声合成して話す機能を実装。
* 音声再生時、音声のスピードに合わせて文字を表示する機能を実装。
* 電話の内容をログファイルに記録する機能を実装。何を話したか後から見返せるようになる。
