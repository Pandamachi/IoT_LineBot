# -*- coding: UTF-8 -*-
import time, threading
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError 
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import config
import DAN
import crawl_weather_V8 as crawl

line_bot_api = LineBotApi('V8eCFtknMyxun7qLhYa3/TPyf7JbY4vplwedLYZPtuGimD5PR/SBQNFU3tmpip+GN27Mfd10tl7SAcVtC/kLhhctJmD/YMyFaDJ3FKwaE3qomT4OgtVR02s0qq5VqsLJBsDv6E+7jxbDxyVOFc4A6gdB04t89/1O/w1cDnyilFU=') #LineBot's Channel access token
handler = WebhookHandler('ac5a5f266dec453f064e9a16642d054c')       #LineBot's Channel secret
user_id_set=set()                                    #LineBot's Friend's user id 
app = Flask(__name__)

ServerURL = 'https://7.iottalk.tw' #with SSL connection
Reg_addr = None #if None, Reg_addr = MAC addreSss

DAN.profile['dm_name']='097linebot'
DAN.profile['df_list']=['mes','mes_o']
DAN.profile['d_name']= '097LineBot'
DAN.device_registration_with_retry(ServerURL, Reg_addr)


def loadUserId():
    try:
        idFile = open(config.idfilePath, 'r')
        idList = idFile.readlines()
        idFile.close()
        idList = idList[0].split(';')
        idList.pop()
        return idList
    except Exception as e:
        print(e)
        return None

def saveUserId(userId):
        idFile = open(config.idfilePath, 'a')
        idFile.write(userId+';')
        idFile.close()


def pushLineMsg(Msg):
    for userId in user_id_set:
        try:
            line_bot_api.push_message(userId, TextSendMessage(text=Msg))
        except Exception as e:
            print(e)
        print('PushMsg: {}'.format(Msg))


@app.route("/", methods=['GET'])
def hello():
    return "HTTPS Test OK."

@app.route("/", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']    # get X-Line-Signature header value
    body = request.get_data(as_text=True)              # get request body as text
    #print("Request body: " + body, "Signature: " + signature)
    try:
        handler.handle(body, signature)                # handle webhook body
    except InvalidSignatureError:
        abort(400)
    return 'OK'

msg_queue = []
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global user_id_set
    Msg = event.message.text
    print(Msg)
#    if Msg == 'Hello, world': return
    if Msg == "溫度":
        print("溫度")
        crawl.getdata()
        DAN.push('mes', crawl.temp[0])
        time.sleep(0.5)
        Odf = DAN.pull('mes_o')
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=Odf[0]))
    if Msg == "天氣":
        print("天氣")
        crawl.getdata()
        DAN.push('mes', crawl.weather[0])
        time.sleep(0.5)
        Odf = DAN.pull('mes_o')
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=Odf[0]))
    if Msg == "風向":
        print("風向")
        crawl.getdata()
        DAN.push('mes', crawl.wind_direction[0])
        time.sleep(0.5)
        Odf = DAN.pull('mes_o')
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=Odf[0]))
    if Msg == "能見度":
        print("能見度")
        crawl.getdata()
        DAN.push('mes', crawl.visible[0])
        time.sleep(0.5)
        Odf = DAN.pull('mes_o')
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=Odf[0]))
    if Msg == "濕度":
        print("濕度")
        crawl.getdata()
        DAN.push('mes', crawl.hum[0])
        time.sleep(0.5)
        Odf = DAN.pull('mes_o')
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=Odf[0]))
    if Msg == "氣壓":
        print("氣壓")
        crawl.getdata()
        DAN.push('mes', crawl.pre[0])
        time.sleep(0.5)
        Odf = DAN.pull('mes_o')
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=Odf[0]))
    if Msg == "降雨量":
        print("降雨量")
        crawl.getdata()
        DAN.push('mes', crawl.rain[0])
        time.sleep(0.5)
        Odf = DAN.pull('mes_o')
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=Odf[0]))
    if Msg == "日照":
        print("日照")
        crawl.getdata()
        DAN.push('mes', crawl.sunlight[0])
        time.sleep(0.5)
        Odf = DAN.pull('mes_o')
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=Odf[0]))
    else:
        print("other")
        # DAN.push("mes", "請輸入：溫度、天氣、風向、能見度、濕度、氣壓、降雨量、日照，來獲得即時氣象資訊")
        # time.sleep(0.5)
        # Odf = DAN.pull('mes_o')
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="請輸入：溫度、天氣、風向、能見度、濕度、氣壓、降雨量、日照，來獲得即時氣象資訊"))

    # print('Incoming Msg: {}'.format(Msg))
    msg_queue.append(Msg)
    userId = event.source.user_id
    if not userId in user_id_set:
        user_id_set.add(userId)
        saveUserId(userId)
    #line_bot_api.reply_message(event.reply_token,TextSendMessage(text="收到訊息!!"))   # reply api example

def init(port=32768):    
    pushLineMsg('LineBot is ready.')
    app.run('127.0.0.1', port=port, threaded=True, use_reloader=False)

idList = loadUserId()
if idList: user_id_set = set(idList)                   
if __name__ == "__main__":
    init()
    

    
