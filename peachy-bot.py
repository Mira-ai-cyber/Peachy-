from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = Flask(__name__)

import os  # ←これを一番上あたりに追加する！

# 環境変数からLINEの情報を読み込む
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text.lower()

    if 'おはよう' in user_message:
        reply = "Peachyから今日の応援メッセージ！\n小さな一歩でも本当にえらいよ🩷今日も一緒にがんばろっ🍑"

    elif '夜' in user_message or 'おつかれ' in user_message:
        reply = "今日も一日おつかれさま🫶\n寝る前に理想のプリケツ🍑や夢が叶った自分を想像してハッピー気分でおやすみしてね✨"

    elif '食事' in user_message:
        reply = "🍽️朝はたんぱく質モリモリ食べてね！卵、サラダチキン、ヨーグルトがおすすめ🩷先にサラダを食べると吸収されにくいよ！"

    else:
        reply = "Peachyだよ🩷なんでも話してね〜！\n『おはよう』『夜』『食事』って言うと、特別メッセージが届くよ🍑"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
