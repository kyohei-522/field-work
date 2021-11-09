# -*- coding: utf-8 -*-
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import seeed_dht
from gpiozero import MCP3002
from gpiozero.pins.pigpio import PiGPIOFactory

import json
import requests

app = Flask(__name__)

line_bot_api = LineBotApi('CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('CHANNEL_SECRET')

url = requests.get('https://www.jma.go.jp/bosai/forecast/data/forecast/010000.json')
text = url.text

data = json.loads(text)
place = '東京'

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    lineRes = event.message.text
    if lineRes == 'temp':
        botRes = getData('temp')

    elif lineRes == 'humi':
        botRes = getData('humi')

    elif lineRes == 'dirt':
        botRes = getDirt('dirt')
        
    elif lineRes == 'weather':
        botRes = getWeather('weather')
    elif lineRes == 'area':
        botRes = '現在の設定地域:' + place
    else:
        botRes ='temp:現在の気温を返します\ndirt:現在の土のしめり具合を返します\nhumi:現在の湿度を返します　\
                \narea:現在の設定地域を返します\nweather:設定地域の２日後までの天気予報を返します'


    line_bot_api.reply_message(
    event.reply_token,
    TextSendMessage(text=botRes))

def getData(arg1):   # require "temp" or "humi"
    i = 0
    try:
        while True:
            if i >= 3:
                raise ValueError('error!')
            i += 1
            sensor = seeed_dht.DHT('22',12)
            humi, temp = sensor.read()
            temp = round(temp,1)
            humi = round(humi,1)
            print(temp)
            print(humi)
            if temp != 0.0:
                print('success!')
                break
            else:
                print('continue')

        if arg1 == 'temp':
            return '気温:' + str(temp) + '°C'
        elif arg1== 'humi':
            return '湿度:' + str(humi) + '%'
        else:
            return '引数が不正です'

    except ValueError as e:
        print('ERROR!')
        return '値を取得できませんでした。実行し直してください'

def getDirt(dirt):
    # 初期化
    Vref = 3.3
    factory = PiGPIOFactory()
    adc_ch0 = MCP3002(channel=0, max_voltage=Vref, pin_factory=factory)
    dirt = adc_ch0.value
    print(dirt)
    if dirt <= 0.5 :
        return '土は十分に湿っています'
    else:
        return '土が乾いています。水やりが必要です'

def getWeather(weather):
    
    weatherData = []
    #当日から２日後までの天気を取得
    selected_areas = [a for a in data if a['name'] == place]
    if selected_areas != []:
        area = selected_areas[0]
        name = area['name']
        print("[", name, "]")
        for ts in area['srf']['timeSeries']:
            times = [n for n in ts['timeDefines']]
            if 'weathers' in ts['areas']:
                for i,v in enumerate(ts['areas']['weathers']):
                    weatherData += (times[i], v)
    else:
        return('その場所のデータは存在しません')
    
    print ('\n'.join(weatherData))
    return place + 'の天気\n' + ('\n'.join(weatherData))

if __name__ == '__main__':
    app.run()