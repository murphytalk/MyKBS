from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import sys
import os
import random
import json


bot_name = 'ころん君'

auto_reply = [
    '我是个安静的倾听者',
    '。。。',
    'そんなの関係ない',
    '我听着呢',
]

app = Flask(__name__)

save_msg = None

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


#@app.route("/callback", methods=['POST'])
@app.route("/", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        msg = json.loads(body)
        if save_msg:
            msg['_incoming'] = True
            save_msg(msg)
        handler.handle(body, signature)
    except InvalidSignatureError as e:
        print(e)
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text

    if bot_name in user_message or '@All' in user_message:
        response_message = random.choice(auto_reply)
        # Send the response message
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response_message))

def run(save_msg_callback):
    global save_msg
    save_msg = save_msg_callback
    app.run()
