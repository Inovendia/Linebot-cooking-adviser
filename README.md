<h2>LINE レシピ推奨ボット</h2>

このプロジェクトは、LINE Messaging API と OpenAI API を活用した、ユーザーの好みに基づくレシピを推奨するLINEボットです！

<h3>機能概要</h3>

ユーザーのLINE入力を元に、
OpenAI API (例: chat.completions.create) を用いてレシピを生成。
食材や風味、予算に基づきカスタマイズができるbot

<h3>システム構成図</h3>
<br>

![Image](https://github.com/user-attachments/assets/893c8d8a-ed06-4379-9251-f56cb9b180da)


<h3>デモ現在の流れ</h3>
<br>
ユーザーがLINEで「気分」や「予算」を選択
LINE Botが追加質問
すべての情報が集まったらOpenAIにレシピ作成を依頼
LINEに推奨レシピを返信
<br>
<h3>bot使用イメージ</h3>
<div style="display: flex; gap: 10px;">
  <img src="https://github.com/user-attachments/assets/a86cc692-5c36-4919-89cc-b89a34e25544" width="25%">
  <img src="https://github.com/user-attachments/assets/7eb237f1-225a-4e4d-b110-005658b6daa7" width="25%">
  <img src="https://github.com/user-attachments/assets/0515c8e7-f63a-4a67-8330-038f3c1e25b7" width="25%">
</div>
<br>
<br>

<h3>開発環境</h3>
<br>
Python 3.x
ライブラリ:
line-bot-sdk
openai
API:
LINE Messaging API
OpenAI API
<br>
**インストール**
<br>
1. Python 環境の準備

Python 3.x をインストール
https://www.python.org

2. 依存ライブラリのインストール

```
pip install line-bot-sdk openai
```

または requirements.txt を使用:

```
pip install -r requirements.txt
```

3. 環境変数の設定

LINE_CHANNEL_SECRET
LINE_CHANNEL_ACCESS_TOKEN
OPEN_AI_KEY
→ LINE Developers & OpenAI ダッシュボードで発行

<h3>AWS Lambda での動作 (オプション)**

Lambda にデプロイ
API Gateway でHTTPSエンドポイントを指定
LINEのWebhook URLにそれを設定
<br>
<h3>使用法</h3>
<br>
イベントフロー:
「気分」や「ジャンル」をLINEで選択
「予算」や「味の好み」(辛い、甘い等)を続けて選択
OpenAI が最適なレシピを生成
<br>
<h3>ファイル構成</h3>
```
.
├── lambda_function.py
├── requirements.txt
├── README.md
```

<h3>今後の課題</h3>
<br>
リッチメニューのデザイン<br>
chatgptのプロンプト内容<br>
画像認識による冷蔵庫の中身からの提案

