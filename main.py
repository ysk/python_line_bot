from flask import Flask, request, abort
from flask_ngrok import run_with_ngrok
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookHandler
from linebot.api import LineBotApi
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import pya3rt
import os

app = Flask(__name__)

run_with_ngrok(app)
load_dotenv()

A3RT_API_KEY       = os.environ['A3RT_API_KEY']
CHANNEL_ACCESS_KEY = os.environ['CHANNEL_ACCESS_KEY']
CHANNEL_SECRET_KEY = os.environ['CHANNEL_SECRET_KEY']
linebot_api = LineBotApi(CHANNEL_ACCESS_KEY)
handler     = WebhookHandler(CHANNEL_SECRET_KEY)


@app.route('/callback', methods=['POST'])
def callback():
  signature = request.headers['X-Line-Signature']
  body = request.get_data(as_text=True)
  try:
    handler.handle(body, signature)
  except InvalidSignatureError:
    abort(400)
  return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_massage(event):
  ai_message = talk_api(event.message.text)
  linebot_api.reply_message(event.reply_token, TextMessage(text=ai_message))


def talk_api(word):
  client = pya3rt.TalkClient(A3RT_API_KEY)
  replay_message = client.talk(word)
  return replay_message['results'][0]['reply']


if __name__ == '__main__':
  app.run()

