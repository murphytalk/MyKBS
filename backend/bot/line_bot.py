from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, VideoMessage , ImageMessage
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

def save_multimedia_file(message_id,content):
    photos_dir = os.getenv('LINE_IMG_DIR','.')
    filename = f'{photos_dir}/{message_id}.{content.content_type.split("/")[1]}'
    print(f'saving {filename}...')
    with open(filename, 'wb') as f:
        for chunk in content.iter_content():
            f.write(chunk)

@handler.add(MessageEvent, message=VideoMessage)
def handle_video_message(event):
    message_id = event.message.id  # Get the ID of the video message
    video_content = line_bot_api.get_message_content(message_id)

    # Process the video content
    # You can save it to a file or perform further operations
    print(f'got video message with id: {message_id} and content-type: {video_content.content_type}')
    save_multimedia_file(message_id,video_content)

@handler.add(MessageEvent, message=ImageMessage)
def handle_img_message(event):
    message_id = event.message.id
    img_content = line_bot_api.get_message_content(message_id)

    print(f'got video message with id: {message_id} and content-type: {img_content.content_type}')
    save_multimedia_file(message_id,img_content)

def run(save_msg_callback):
    global save_msg
    save_msg = save_msg_callback
    app.run()
