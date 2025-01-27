import requests
import json
import os

# チャネルアクセストークン
CHANNEL_ACCESS_TOKEN = os.getenv('CHANNEL_ACCESS_TOKEN')

# リッチメニュー作成APIエンドポイント
url = "https://api.line.me/v2/bot/richmenu"

# リッチメニューのデータ
headers = {
    "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

richmenu_body = {
    "size": {
        "width": 2500,
        "height": 1686
    },
    "selected": True,
    "name": "Nice rich menu",
    "chatBarText": "Tap to open",
    "areas": [
        {
            "bounds": {
                "x": 0,
                "y": 0,
                "width": 1250,
                "height": 843
            },
            "action": {
                "type": "postback",
                "label": "leftovers",
                "data": "tap_leftovers",
                "text": "送信中"
                #"displayText": "冷蔵庫から"
            }
        },
        {
            "bounds": {
                "x": 1251,
                "y": 0,
                "width": 1250,
                "height": 843
            },
            "action": {
                "type": "postback",
                "label": "suggestion",
                "data": "tap_suggestion",
                "text": "送信中"
                #"displayText": "提案希望"
            }
        },
        {
            "bounds": {
                "x": 0,
                "y": 844,
                "width": 1250,
                "height": 843
            },
            "action": {
                "type": "postback",
                "label": "scene",
                "data": "tap_scene",
                "text": "送信中"
                #"displayText": "シーン"
            }
        },
        {
            "bounds": {
                "x": 1251,
                "y": 844,
                "width": 1250,
                "height": 843
            },
            "action": {
                "type": "uri",
                "label": "link",
                "uri": "https://www.kurashiru.com/"
            }
        }

    ]
}

# rich_menu_id = ""

# APIリクエストを送信
response = requests.post(url, headers=headers, data=json.dumps(richmenu_body))
# 結果を表示
if response.status_code == 200:
    rich_menu_id = response.json()["richMenuId"]
    print("リッチメニューが作成されました")
    print("リッチメニューID:", rich_menu_id)
else:
    print("エラーが発生しました:", response.status_code, response.text)

#rich menuの画像を送信

def upload_richmenu_image(rich_menu_id, image_path):
    #print("リッチメニューID:", rich_menu_id)
    # リッチメニュー画像アップロードAPIエンドポイント
    url = f"https://api-data.line.me/v2/bot/richmenu/{rich_menu_id}/content"
    headers = {
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}",
        "Content-Type": "image/png"
    }
    # 画像データを送信
    with open(image_path, "rb") as image_file:
        response = requests.post(url, headers=headers, data=image_file)

    # 結果を表示
    if response.status_code == 200:
        print("画像がアップロードされました")
    else:
        print("画像アップロード中にエラーが発生しました:", response.status_code, response.text)

# 例: リッチメニューIDと画像パスを指定して呼び出す
image_path = "/Users/nakagawaissei/Downloads/menu1-min.png"
upload_richmenu_image(rich_menu_id, image_path)

#リッチメニューを設定する
url = f"https://api.line.me/v2/bot/user/all/richmenu/{rich_menu_id}"
headers = {
    "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}"
}

# リクエストを送信
response = requests.post(url, headers=headers)

# 結果の表示
if response.status_code == 200:
    print("リッチメニューがすべてのユーザーに適用されました")
else:
    print(f"リッチメニュー適用失敗: {response.status_code} - {response.text}")

