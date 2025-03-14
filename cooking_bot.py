import os
import json
import openai

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    MessageEvent, TextMessage, ImageMessage,TextSendMessage,FollowEvent,ImageSendMessage,
    TemplateSendMessage,ButtonsTemplate,PostbackAction,FlexSendMessage,URIAction,MessageTemplateAction,
    ImagemapSendMessage,BaseSize,URIImagemapAction,ImagemapArea,PostbackEvent,ImageCarouselTemplate,
    ImageCarouselColumn,RichMenu,QuickReply,QuickReplyButton,MessageAction
)

handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
openai.api_key= os.getenv('OPEN_AI_KEY')

#やりたいこと
#家族情報を入力してもらって保存しておく→提案する料理内容もカスタマイズできて良い
#野菜価格のAPIを使って、より正確な提案とか安い野菜を使った提案ができれば素晴らしい

def lambda_handler(event, context):
    #print(event)
    #リクエストに成功した時のheaders(ヘッダー)とbody(本文)の値を取り出して引数にしている
    headers = event["headers"]
    body = event["body"]

    signature = headers["x-line-signature"]#headersの署名のx-lineを取り出して引数にしている

    handler.handle(body, signature)

    return {"statusCode": 200, "body": "OK"}


user_data = {}

@handler.add(PostbackEvent)
@handler.add(MessageEvent, message=TextMessage)

def handle_event(event):
    print(event)
    user_id=event.source.user_id #共通データ格納
    postback_data = None
    postback_data_t = None
    feeling = user_data.get(user_id, {}).get("feeling", None)
    scene = user_data.get(user_id, {}).get("scene", None)

    if isinstance(event, PostbackEvent):
        postback_data = event.postback.data
        #-----アレンジ部分、消すならここから下-------
        if postback_data == "tap_leftovers":
            image_url_1 = ("https://drive.usercontent.google.com/download?id=1bJk6FZB7KALecEYGEs74hXNPkP1UeLfB&export=view&authuser=0")
            start_event = [
                    TemplateSendMessage
                    (
                        alt_text="EmotionalButton",
                        template=ButtonsTemplate
                        (
                            thumbnail_image_url = image_url_1,
                            title="気分に沿った提案もできるよ",
                            text='▼ どうする？ ▼',
                            actions=
                                [
                                    PostbackAction(label="気分を教える", data="気分を教える", text="送信中"),
                                    PostbackAction(label="アイデアだけ欲しい", data="アイデアだけ欲しい", text="送信中"),
                                ]
                        )
                    )
                ]
            line_bot_api.reply_message(
                event.reply_token,start_event
            )
        elif postback_data == "気分を教える":
            second_message = [
                TextSendMessage(
                    text="気分を考慮した提案をするね"
                ),
                TemplateSendMessage(
                    alt_text='emotion',
                    template=ButtonsTemplate(
                        title="今どんな気分？",
                        text='▼ タップして選ぶ ▼',
                        actions=[
                            PostbackAction(label="いつも通り", data="気分はいつも通り", text="送信中"),
                            PostbackAction(label="楽したい", data="楽したい", text="送信中"),
                            PostbackAction(label="元気になりたい", data="元気になりたい", text="送信中"),
                            PostbackAction(label="凝りたい", data="凝りたい", text="送信中")
                        ]
                    )
                )
            ]
            line_bot_api.reply_message(
                event.reply_token,second_message
            )

        elif postback_data in ["気分はいつも通り","楽したい","元気になりたい","凝りたい"]:
            if user_id not in user_data:
                user_data[user_id] = {}

            user_data[user_id]["feeling"] = postback_data
            second_message = [
                TextSendMessage(
                    text="ありものを入力してね。回答までは少し待ってね。"
                )
            ]
            line_bot_api.reply_message(
                event.reply_token,second_message
            )
            print(user_data)####

        elif postback_data == "アイデアだけ欲しい":
            if user_id not in user_data:
                user_data[user_id] = {}

            user_data[user_id]["feeling"] = postback_data
            second_message = [
                TextSendMessage(
                    text="了解！ありものを入力してね。回答までは少し待ってね。"
                )
            ]
            line_bot_api.reply_message(
                event.reply_token,second_message
            )
            print(user_data)####

        elif postback_data == "tap_suggestion":
            suggest_message = [
                TextSendMessage(
                    text = "これから3つの質問に答えてね"
                ),
                TemplateSendMessage(
                        alt_text='price_range',
                        template=ButtonsTemplate(
                            title="予算はいくら？近いものを選んでね",
                            text='▼ タップして選ぶ ▼',
                            actions=[
                                PostbackAction(label="5000円", data="5000円", text="送信中"),
                                PostbackAction(label="10000円", data="10000円", text="送信中"),
                                PostbackAction(label="15000円", data="15000円", text="送信中"),
                                PostbackAction(label="20000円", data="20000円", text="送信中")
                            ]
                        )
                )
            ]
            line_bot_api.reply_message(
                event.reply_token,suggest_message
            )


        elif postback_data in ["5000円", "10000円", "15000円", "20000円"]:
            if user_id not in user_data:
                user_data[user_id] = {}

            user_data[user_id]["budget"] = postback_data
            quick_reply_buttons = [
            QuickReplyButton(action=PostbackAction(label="辛いもの",data="辛いもの", text="送信中")),
            QuickReplyButton(action=PostbackAction(label="甘いもの",data="甘いもの", text="送信中")),
            QuickReplyButton(action=PostbackAction(label="酸っぱいもの",data="酸っぱいもの", text="送信中")),
            QuickReplyButton(action=PostbackAction(label="苦いもの",data="苦いもの", text="送信中")),
            QuickReplyButton(action=PostbackAction(label="しょっぱいもの",data="しょっぱいもの", text="送信中"))
            ]
            quick_reply = QuickReply(items = quick_reply_buttons)
            quick_message = TextSendMessage(
                text = "好みの味に最も近いものを1つ選んでください",
                quick_reply=quick_reply
            )
            line_bot_api.reply_message(event.reply_token,[quick_message])

        elif postback_data in ["甘いもの","辛いもの","酸っぱいもの","しょっぱいもの","苦いもの"]:
            user_data [user_id]["flavor"]= postback_data
            taste = "味"
            health = "健康"
            looks = "見た目"
            nutrition = "栄養"
            quick_reply_buttons = [
            QuickReplyButton(action=PostbackAction(label=taste,data=taste,text="送信中")),
            QuickReplyButton(action=PostbackAction(label=health,data=health,text="送信中")),
            QuickReplyButton(action=PostbackAction(label=looks,data=looks,text="送信中")),
            QuickReplyButton(action=PostbackAction(label=nutrition,data=nutrition,text="送信中"))
            ]
            quick_reply = QuickReply(items = quick_reply_buttons)
            quick_message = TextSendMessage(
                text = "食事で大切にしていることに最も近いものを1つ選んでください",
                quick_reply=quick_reply
                )
            line_bot_api.reply_message(event.reply_token,[quick_message])

        elif postback_data in ["味","健康","見た目","栄養"]:
            user_data [user_id]["important"] = postback_data
            jap = "和食"
            euro = "洋食"
            chi = "中華料理"
            Kor = "韓国料理"
            other = "多国籍料理"
            quick_reply_buttons = [
            QuickReplyButton(action=PostbackAction(label=jap,data=jap,text="送信中")),
            QuickReplyButton(action=PostbackAction(label=euro,data=euro,text="送信中")),
            QuickReplyButton(action=PostbackAction(label=chi,data=chi,text="送信中")),
            QuickReplyButton(action=PostbackAction(label=Kor,data=Kor,text="送信中")),
            QuickReplyButton(action=PostbackAction(label=other,data=other,text="送信中"))
            ]
            quick_reply = QuickReply(items = quick_reply_buttons)
            quick_message = TextSendMessage(
                text = "最も好きな料理ジャンルを選んでください",
                quick_reply=quick_reply
                )
            line_bot_api.reply_message(event.reply_token,[quick_message])


        elif postback_data in ["和食","洋食","中華料理","韓国料理","多国籍料理"]:
            user_data [user_id]["Genre"]= postback_data
            gar = "にんにく"
            gin = "しょうが"
            hot = "唐辛子"
            mou = "山椒と花椒"
            curry = "カレー粉"
            quick_reply_buttons = [
            QuickReplyButton(action=PostbackAction(label=gar,data=gar,text="送信中")),
            QuickReplyButton(action=PostbackAction(label=gin,data=gin,text="送信中")),
            QuickReplyButton(action=PostbackAction(label=hot,data=hot,text="送信中")),
            QuickReplyButton(action=PostbackAction(label=mou,data=mou,text="送信中")),
            QuickReplyButton(action=PostbackAction(label=curry,data=curry,text="送信中"))
            ]
            quick_reply = QuickReply(items = quick_reply_buttons)
            quick_message = TextSendMessage(
                text = "最も好きなスパイスを選んでください",
                quick_reply=quick_reply
                )
            line_bot_api.reply_message(event.reply_token,[quick_message])

        elif postback_data in ["にんにく","しょうが","唐辛子","山椒と花椒","カレー粉"]:
            user_data [user_id]["spice"]= postback_data
            balance = "バランスよく"
            bird = "鶏肉をよく"
            pork = "豚肉をよく"
            beef = "牛肉をよく"
            fish = "魚をよく"
            shell = "貝をよく"
            quick_reply_buttons = [
            QuickReplyButton(action=PostbackAction(label="バランスよく",data=balance,text="これから提案するから、少し待っててね")),
            QuickReplyButton(action=PostbackAction(label="鶏肉",data=bird,text="これから提案するから、少し待っててね")),
            QuickReplyButton(action=PostbackAction(label="豚肉",data=pork,text="これから提案するから、少し待っててね")),
            QuickReplyButton(action=PostbackAction(label="牛肉",data=beef,text="これから提案するから、少し待っててね")),
            QuickReplyButton(action=PostbackAction(label="貝",data=shell,text="これから提案するから、少し待っててね")),
            QuickReplyButton(action=PostbackAction(label="魚",data=fish,text="これから提案するから、少し待っててね"))
            ]
            quick_reply = QuickReply(items = quick_reply_buttons)
            quick_message = TextSendMessage(
                text = "肉類・魚介類で好みがあれば教えて下さい",
                quick_reply=quick_reply
                )
            line_bot_api.reply_message(event.reply_token,[quick_message])

        elif postback_data in ["バランスよく","鶏肉をよく","豚肉をよく","牛肉をよく","魚をよく","貝をよく"]:
            user_data [user_id]["meat&fish"]= postback_data # ここでmeat&fishの情報を保存
            user_info = user_data.get(user_id,{})
            meat_and_fish = user_info.get("meat&fish", "未設定")
            budget = user_info.get("budget","未設定")
            flavor = user_info.get("flavor","未設定")
            important = user_info.get("important","未設定")
            Genre = user_info.get("Genre","未設定")
            spice = user_info.get("spice","未設定")
            print(user_info)
            # user_info ["meat&fish"]= postback_data
            messages = [
                {
                    "role": "system",
                    "content":
                    f"あなたはベテランの主婦で料理のレパートリーも多いです。"
                    f"私は{flavor}が好きで、{spice}が効いたものが好きです。"
                    f"料理をする時は{important}に気を遣っています。"
                    f"私が好きな料理のジャンルは{Genre}ですが、他のジャンルの料理も食べます。"
                    f"肉と魚は{meat_and_fish}使います。"
                    f"私の好みに合うように、予算{budget}で1週間の料理の献立を提案して下さい。"
                    f"また、その献立に必要な材料を箇条書きで簡潔に教えて下さい。"
                }
            ]
            try:
                response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=600
                )
                reply_message = response.choices[0].message.content.strip()
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
            except openai.OpenAIError as e:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="提案を生成できませんでした。もう一度試してください。"))
            except Exception as e:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="エラーが発生しました。もう一度試してください。"))

        elif postback_data == "tap_scene":
            # image_url_1 = ("https://drive.usercontent.google.com/download?id=1bJk6FZB7KALecEYGEs74hXNPkP1UeLfB&export=view&authuser=0")
            if user_id not in user_data:
                user_data[user_id] = {}

            scene_event = [
                    TemplateSendMessage
                    (
                        alt_text="SceneButton",
                        template=ButtonsTemplate
                        (
                            # thumbnail_image_url = image_url_1,
                            title="どんなシーンを想定していますか？",
                            text='▼シーンに近いものを選ぶ▼',
                            actions=
                                [
                                    PostbackAction(label="子供と楽しむ", data="子供と楽しむ", text="送信中"),
                                    PostbackAction(label="お酒のおつまみ", data="お酒のおつまみ", text="送信中"),
                                    PostbackAction(label="おもてなしやパーティー", data="おもてなしやパーティー", text="送信中"),
                                    PostbackAction(label="作り置き", data="作り置きを作りたい", text="送信中")
                                ]
                        )
                    )
                ]
            line_bot_api.reply_message(
                event.reply_token,scene_event
            )

        elif postback_data =="作り置きを作りたい":
            user_data[user_id]["feeling"] = postback_data
            which_choice = [
                    TemplateSendMessage
                    (
                        alt_text="choiceButton",
                        template=ButtonsTemplate
                        (
                            # thumbnail_image_url = image_url_1,
                            title="ありもので作りますか？",
                            text='▼選ぶ▼',
                            actions=
                                [
                                    PostbackAction(label="はい", data="はい", text="送信中"),
                                    PostbackAction(label="いいえ、買い出しに行きます", data="いいえ", text="送信中")
                                ]
                        )
                    )
                ]
            line_bot_api.reply_message(
                event.reply_token,which_choice
            )

        elif postback_data == "はい":
            user_data[user_id]["answer"] = postback_data
            second_message = [
                TextSendMessage(
                    text="ありものを入力してね。回答までは少し待ってね。"
                )
            ]
            line_bot_api.reply_message(
                event.reply_token,second_message
            )

        elif postback_data == "いいえ":
            try:
                messagess = [
                {
                    "role": "system", "content": f"あなたはベテランの主婦で料理のレパートリーも多いです。これから料理の作り置きをします。アイデアを5つ提案して下さい"
                }
                ]
                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messagess,
                    max_tokens=500
                )
                reply_message = response.choices[0].message.content.strip()
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
            except openai.OpenAIError as e:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="提案を生成できませんでした。もう一度試してください。"))
            except Exception as e:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="システムエラーが発生しました。開発者にお問い合わせください。"))

        elif postback_data in ["子供と楽しむ","お酒のおつまみ","おもてなしやパーティー"]:
            messages = [
                {
                    "role": "system",
                    "content":
                    "あなたはベテランの主婦で料理のレパートリーも多いです。"
                    "次のシーンに合わせたアイデアやレシピを5つ提案して下さい:"
                    f"{postback_data}"
                }
            ]
            print(messages)
            try:
                response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=600
                )
                reply_message = response.choices[0].message.content.strip()
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
            except openai.OpenAIError as e:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="提案を生成できませんでした。もう一度試してください。"))
            except Exception as e:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="エラーが発生しました。もう一度試してください。"))

        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="初めからやり直して下さい"))


    elif isinstance(event, MessageEvent):
        postback_data_t = event.message.text #textデータをpostback_dataに格納。つまりtextデータも全てpostback_dataとして扱っていい
        #user_input=event.message.text

        if postback_data_t != "送信中" and postback_data_t != "これから提案するから、少し待っててね":
                try:
                    messagess = [
                    {"role": "system", "content": f"あなたはベテランの主婦で料理のレパートリーも多いです。今日は{feeling}です。料理を5つ提案して下さい。"},
                    {"role": "user", "content": postback_data_t},
                    ]
                    response = openai.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=messagess,
                        max_tokens=500
                    )
                    reply_message = response.choices[0].message.content.strip()
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
                except openai.OpenAIError as e:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="提案を生成できませんでした。もう一度試してください。"))
                except Exception as e:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="システムエラーが発生しました。開発者にお問い合わせください。"))

        elif postback_data_t == "送信中" or postback_data_t == "これから提案するから、少し待っててね":
            return


        else:
            return #対応しないイベントなら終了

    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="初めからやり直して下さい"))
