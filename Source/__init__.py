from flask import Flask, request, abort
import requests
import json
from datetime import datetime
from os.path import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
      return 'Nothing at here', 200

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
      if request.method == 'POST':
            # channel_access_token = 'xsaSOYmzmLnG6SVtTR4L7cG6IdP+oOVBvbr4EGdQu2F0YGLvckUJK5kQg9DcHsm/fCTdVIYmA9APd/vni6usLJz7cVExWL13tZYEsmJvriaE3r57NREg3TF0eF0UqQv/bmze9BA/e3ZgTv2dzRDC2AdB04t89/1O/w1cDnyilFU='
            data = json.dumps(request.json['events'])
            time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            dir_name = 'log_alert_line'

            # Create target Directory if don't exist
            if not os.path.exists(dir_name):
                  os.mkdir(dir_name)
                  print("Directory " , dir_name ,  " Created ")

            for data in json.loads(data):
                  # reply_token = data['replyToken']
                  message = data['message']

            if message['type'] == 'sticker':
                  file = open('{}'.format(dir_name) + '/' + 'log_reply_content' + '.txt', 'a')
                  file.write(time + '  ---  ' + '{}'.format(message) + '\n')
            elif message['type'] == 'text':
                  if message['text'].upper() == 'YES':
                        file = open('{}'.format(dir_name) + '/' + 'log_reply_to_splunk' + '.txt', 'a')
                        file.write(time + '  ---  ' + '{}'.format(message['text']) + '\n')
                  else:
                        file = open('{}'.format(dir_name) + '/' + 'log_reply_content' + '.txt', 'a')
                        file.write(time + '  ---  ' + '{}'.format(message) + '\n')

            file.close()

            return request.json, 200
      elif request.method == 'GET':
            return 200

def ReplyMessage(replyToken, textMessage, channelAcessToken):
      LINE_API = 'https://api.line.me/v2/bot/message/reply'

      authorization = 'Bearer {}'.format(channelAcessToken)

      headers = {
            'Content-Type' : 'application/json; charset=UTF-8',
            'Authorization' : authorization
      }

      data = {
            "replyToken" : replyToken,
            "messages" : [{
            "type": "template",
            "altText": "This is a buttons template",
            "template": {
                  "type": "buttons",
                  "thumbnailImageUrl": "https://smartnet.net.vn/wp-content/uploads/2019/04/default-blogpost-image.jpg",
                  "imageAspectRatio": "rectangle",
                  "imageSize": "cover",
                  "imageBackgroundColor": "#FFFFFF",
                  "title": "Menu",
                  "text": "Please select",
                  "defaultAction": {
                  "type": "uri",
                  "label": "View detail",
                  "uri": "http://example.com/page/123"
                  },
                  "actions": [
                  {
                        "type": "postback",
                        "label": "Block request",
                        "data": "action=buy&itemid=123"
                  },
                  {
                        "type": "uri",
                        "label": "View detail",
                        "uri": "https://smartnet.net.vn/wp-content/uploads/2019/04/default-blogpost-image.jpg"
                  }
                  ]
            }
            }]
      }

      data = json.dumps(data)
      requests.post(LINE_API, headers = headers, data = data)
      return 200