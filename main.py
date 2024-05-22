import configparser

config = configparser.ConfigParser()
config.read('config.ini')
line_token = str(config['LINEBOT']['ChannelToken'])
line_secret = str(config['LINEBOT']['ChannelSecret'])

from flask import Flask, request, abort
import warnings
from linebot import LineBotSdkDeprecatedIn30
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from data_handler import DataHandler
from textwrap import dedent
from misc import lang_table
ltb = lang_table[str(config['LANGUAGE']['Language'])]

app = Flask(__name__)

line_bot_api = LineBotApi(line_token)
handler = WebhookHandler(line_secret)

dh = DataHandler()
dh.load_data()

@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info('Request body: ' + body)
    print(body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print('Invalid signature. Please check your channel access token/channel secret.')
        abort(400)
    return 'OK'

# Message event
@handler.add(MessageEvent)
def handle_message(event):
    message_type = event.message.type
    user_id = event.source.user_id
    reply_token = event.reply_token
    message = event.message.text
    line_bot_api.reply_message(reply_token, TextSendMessage(text = message))

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    # 當收到文字消息時，發送一個請求位置的按鈕消息
    if event.message.text == ltb['HI_MSG']:
        buttons_template = ButtonsTemplate(
            title=ltb['LOCATION_REQ_TITLE'], text=ltb['LOCATION_REQ_TEXT'], actions=[
                LocationAction(label=ltb['LOCATION_REQ_LABEL'])
            ]
        )
        template_message = TemplateSendMessage(
            alt_text=ltb['LOCATION_REQ_TITLE'], template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ltb['LOCATION_REQ_HINT']))

@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    # 當收到位置消息時，回復經緯度資訊
    latitude = event.message.latitude
    longitude = event.message.longitude
    
    type, coord, addr, floors, cap, auth, dist = dh.find_closest(latitude, longitude)

    # google_maps_url = f'https://www.google.com/maps/search/?api=1&query={eval(coord)[0]},{eval(coord)[1]}'

    label_width = 12
    reply_text = (
        "{} {:.4f},{:.4f}\n\n"
        "{}\n"
        "{:<{width}}\n\t{}\n"
        "{:<{width}}\n\t{:.4f},{:.4f}\n"
        "{:<{width}}\n\t{}\n"
        "{:<{width}}\n\t{}\n"
        "{:<{width}}\n\t{}\n"
        "{:<{width}}\n\t{:.4f} {}"
    ).format(
        ltb['LOC_REPLY_YOURS'],
        latitude, longitude,
        ltb['LOC_REPLY_CLOSEST_BUILDING'],
        ltb['LOC_TYPE'], type,
        ltb['LOC_COORD'], eval(coord)[0], eval(coord)[1],
        ltb['LOC_FLOOR'], floors,
        ltb['LOC_CAP'], cap,
        ltb['LOC_AUTH'], auth,
        ltb['LOC_DIST'], dist, ltb['LOC_KM'],
        width=label_width
    )
    
    print(reply_text)

    text_message = TextSendMessage(text=reply_text)
    location_message = LocationSendMessage(
        title = addr if addr else 'No address provided',
        address = addr if addr else 'No address provided',
        latitude = eval(coord)[0],
        longitude = eval(coord)[1]
    )

    line_bot_api.reply_message(event.reply_token, [text_message, location_message])


import os
if __name__ == "__main__":

    warnings.filterwarnings("ignore", category=LineBotSdkDeprecatedIn30)
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)
