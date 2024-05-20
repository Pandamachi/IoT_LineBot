# -*- coding: UTF-8 -*-

#Python module requirement: line-bot-sdk, flask
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError 
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import crawl_weather_V8 as crawl
import config
import DAN

line_bot_api = LineBotApi('896u1fmFboLXaCNPvrsrq3jwOGO8zu1FvbGWG78PRRoYjpNi/yRsATadrhtbPwDON27Mfd10tl7SAcVtC/kLhhctJmD/YMyFaDJ3FKwaE3pZ3ozEpThiwFF6tYPaq9qrtrHdbLKbHdAUx0s1pWGcVQdB04t89/1O/w1cDnyilFU=') #LineBot's Channel access token
handler = WebhookHandler('ac5a5f266dec453f064e9a16642d054c')        #LineBot's Channel secret
user_id_set=set()                                         #LineBot's Friend's user id 
app = Flask(__name__)

ServerURL = 'https://3.iottalk.tw' #with SSL connection
Reg_addr = 'C0:98:E5:00:00:97' #if None, Reg_addr = MAC address

DAN.profile['dm_name']='097linebot'
DAN.profile['df_list']=['mes','mes_o']
DAN.profile['d_name']= '097LineBot'
DAN.device_registration_with_retry(ServerURL, Reg_addr)

def loadUserId():
    try:
        idFile = open('idfile', 'r')
        idList = idFile.readlines()
        idFile.close()
        idList = idList[0].split(';')
        idList.pop()
        return idList
    except Exception as e:
        print(e)
        return None

def saveUserId(userId):
        idFile = open('idfile', 'a')
        idFile.write(userId+';')
        idFile.close()


@app.route("/", methods=['GET'])
def hello():
    return "HTTPS Test OK."

@app.route("/", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']    # get X-Line-Signature header value
    body = request.get_data(as_text=True)              # get request body as text
    print("Request body: " + body, "Signature: " + signature)
    try:
        handler.handle(body, signature)                # handle webhook body
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    Msg = event.message.text
    if Msg == 'Hello, world': return
    print('GotMsg:{}'.format(Msg))

    line_bot_api.reply_message(event.reply_token,TextSendMessage(text="收到訊息!!"))   # Reply API example
    
    userId = event.source.user_id
    if not userId in user_id_set:
        user_id_set.add(userId)
        saveUserId(userId)

   
if __name__ == "__main__":

    idList = loadUserId()
    if idList: user_id_set = set(idList)

    try:
        for userId in user_id_set:
            line_bot_api.push_message(userId, TextSendMessage(text='LineBot is ready for you.'))  # Push API example
    except Exception as e:
        print(e)
    
    app.run('127.0.0.1', port=32768, threaded=True, use_reloader=False)

    

