🍜 LINE レシピ推奨ボット

このプロジェクトは、LINE Messaging API と OpenAI API を活用した、ユーザーの好みに基づくレシピを推奨するLINEボットです！

**機能概要**

ユーザーのLINE入力を元に、
OpenAI API (例: chat.completions.create) を用いてレシピを生成。
食材や風味、予算に基づきカスタマイズができるbot

**システム構成図**


![Image](https://github.com/user-attachments/assets/893c8d8a-ed06-4379-9251-f56cb9b180da)


**デモ現在の流れ**

ユーザーがLINEで「気分」や「予算」を選択
LINE Botが追加質問
すべての情報が集まったらOpenAIにレシピ作成を依頼
LINEに推奨レシピを返信

**開発環境**

Python 3.x
ライブラリ:
line-bot-sdk
openai
API:
LINE Messaging API
OpenAI API

**インストール**

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

**AWS Lambda での動作 (オプション)**

Lambda にデプロイ
API Gateway でHTTPSエンドポイントを指定
LINEのWebhook URLにそれを設定

**使用法**

イベントフロー:
「気分」や「ジャンル」をLINEで選択
「予算」や「味の好み」(辛い、甘い等)を続けて選択
OpenAI が最適なレシピを生成

**ファイル構成**
```
.
├── lambda_function.py
├── requirements.txt
├── README.md
```

**未定の部分**

リッチメニューのデザイン
chatgptのプロンプト内容
画像認識による冷蔵庫の中身からの提案

