import json
from linebot import LineBotApi
from linebot.models import TextSendMessage
import requests
from bs4 import BeautifulSoup
import os

file = open('info.json','r')
info = json.load(file)

CHANNEL_ACCESS_TOKEN = info["CHANNEL_ACCESS_TOKEN"]
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)

def get_latest_ep():#話数を取得
    load_url = "https://bushoryu.github.io/busho_ryu/infoTab.html"
    html = requests.get(load_url)
    soup = BeautifulSoup(html.content, "html.parser")
    
    for element in soup.find_all("dd"):    # すべてのaタグを検索して表示
        if "『" and "』" in element.text:
            latest_ep = element.text
        return latest_ep
# def get_latest_no():#数を取得
#     for element in soup.find_all("a"):    # すべてのaタグを検索して表示
#         if "info" and "." in element.text:
#             latest_no = element.text
#             print(latest_no)
#         return latest_no

def send_line(texts):#ライン送信
    USER_ID = info["USER_ID"]
    messages = TextSendMessage(text="お知らせが来ました！"+texts+"https://bushoryu.github.io/busho_ryu/infoTab.html")
    line_bot_api.push_message(USER_ID, messages=messages)
    
def log_check(content):#最新話かどうか判定
    
    logfile_name = "HP_New.txt"
    if not os.path.exists("./"+logfile_name):#ログファイルの存在を確認
        file = open(logfile_name, 'w')#なければ作る
    file = open(logfile_name, 'r')#読み取りでファイルを開く
    if file.read() == content:
        checker = False
        print(content+" ng")
    else:
        checker = True
        file = open(logfile_name, 'w')
        file.write(content)
        file.close()   
        print(content)

    return checker

if __name__ == "__main__":
    latest_episode = get_latest_ep()
    # latest_episode_no = get_latest_no()
    if log_check(latest_episode):
        send_line(latest_episode)