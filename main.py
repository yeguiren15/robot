import pyaudio
import wave
import win32com.client
from aip import AipSpeech
from bs4 import BeautifulSoup
import requests
import chardet
from lxml import etree
import pyttsx3
import pygame
import time

speaker = win32com.client.Dispatch("SAPI.SpVoice")
def record(file_path):
    # 各路参数
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = file_path
    pau = pyaudio.PyAudio()
    stream = pau.open(format=FORMAT,
                      channels=CHANNELS,
                      rate=RATE,
                      input=True,
                      frames_per_buffer=CHUNK, )
    frames = []
    print("开始录音")
    speaker.Speak("开始录音")
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("录音结束")
    speaker.Speak("录音结束")
    stream.stop_stream()
    stream.close()
    pau.terminate()
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(pau.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
def voice2text(APP_ID, API_KEY, SECRET_KEY, file_path):
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    ret = client.asr(get_data(file_path), 'pcm', 16000, {'dev_pid': 1537}, )
    print(ret)
    return ret['result']

def get_data(file_path):
    with open(file_path, 'rb') as fp:
        return fp.read()
#人机互动
import requests
import time
import pygame
import requests
import pyttsx3
engine = pyttsx3.init()
# 向api发送请求
def get_response(msg):
    msg = str(msg)
    url = 'http://api.qingyunke.com/api.php?key=free&appid=0&msg={}'.format(urllib.parse.quote(msg))
    try:
        answer = requests.get(url)
        engine = pyttsx3.init()
        engine.say(answer.json()["content"])
        engine.runAndWait()
        print(answer.json()["content"])
    except:
        return
def say():
    global chat_message
    # 存放的文件名称
    file_path = "data/chat-audio.wav"
    # 百度需要的参数
    APP_ID = '31748890'
    API_KEY = 'INDF9ODyUhLg371ySlTSwyBZ'
    SECRET_KEY = 'XAxq2OOgDNFFtDc2weFCAtrwVXA1iorG'
    # 先调用录音函数
    record(file_path)
    # 语音转成文字的内容
    chat_message = voice2text(APP_ID, API_KEY, SECRET_KEY, file_path)
    print(chat_message)


def chatwithrobot():
    i=0
    while i<1:
        say()
        get_response(chat_message)
        i=i+1

#音乐播放
import base64
import random
from binascii import hexlify
from Crypto.Cipher import AES
import json
import requests
import urllib, requests
import pyttsx3
import pygame
class GetMusic:
    def __init__(self):
        self.key = GetParamsAndEncSecKey()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
            'Referer': 'http://music.163.com/'}
        self.session = requests.Session()
        self.session.headers = self.headers
        self.conmment_url = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_{}?csrf_token='  # 评论
        self.lyric_url = 'https://music.163.com/weapi/song/lyric?csrf_token='  # 歌词
        self.music_url = 'https://music.163.com/weapi/song/enhance/player/url?csrf_token='  # 歌曲
        self.url = 'https://music.163.com/weapi/cloudsearch/get/web?csrf_token='  # 搜索歌曲列表，无歌曲链接
    def get_params_and_encSecKey(self, song=None):
        '''
        获取什么就返回所需要两个参数
        1. 歌曲
        2. 歌词
        3. 评论  默认
        4. 搜索的歌曲列表
        :param song:
        :return:
        '''
        if isinstance(song, int):
            data = {"ids": [song], "br": 128000, "csrf_token": ""}
        elif isinstance(song, str) and song.isdigit():
            data = {"id": song, "lv": -1, "tv": -1, "csrf_token": ""}
        elif song == None:
            data = {}
        else:
            data = {"hlpretag": "<span class=\"s-fc7\">", "hlposttag": "</span>", "s": song, "type": "1", "offset": "0",
                    "total": "true", "limit": "30", "csrf_token": ""}
        song = json.dumps(data)
        data = self.key.get(song)
        return data
    def get_music_list_info(self, name):
        '''
        获取歌曲详情：歌名+歌曲id+作者
        :param name:
        :return:
        '''
        data = self.get_params_and_encSecKey(name)
        res = self.session.post(self.url, data=data)  # 歌曲
        song_info = res.json()['result']['songs']
        for song in song_info:
            song_name = song['name']
            song_id = song['id']
            songer = song['ar'][0]['name']
            print(song_name, '\t', song_id, '\t', songer)
            global SongName  # 定义为全局变量
            global SongId  # 定义为全局变量
            global Songer  # 定义为全局变量
            SongName=song_name
            SongId=song_id
            Songer=songer
            self.get_music_url(song_id)
            self.get_music_lyric(song_id)
            self.get_music_comment(song_id)
            break
    def get_music_url(self, id):
        '''
        获取歌曲URL链接
        :param id:
        :return:
        '''
        global Song_url  # 定义为全局变量
        data = self.get_params_and_encSecKey(id)
        res = self.session.post(self.music_url, data=data)
        song_url = res.json()['data'][0]['url']
        Song_url=song_url
        #print(song_url)
    def get_music_lyric(self, id_str):
        '''
        获取歌词
        :param id_str:
        :return:
        '''
        data = self.get_params_and_encSecKey(str(id_str))
        res = self.session.post(self.lyric_url, data=data)
        lyric = res.json()['lrc']['lyric']
        #print(lyric)
    def get_music_comment(self, song_id):
        '''
        获取歌曲评论: 评论人+内容+头像
        :param song_id:
        :return:
        '''
        data = self.get_params_and_encSecKey()
        comment = self.session.post(self.conmment_url.format(str(song_id)), data=data)
        com_list = comment.json()['hotComments']
        for com in com_list:
            content = com['content']
            nickname = com['user']['nickname']
            user_img = com['user']['avatarUrl']
            #print(nickname, '!!!!' + content + '!!!!', user_img)
class GetParamsAndEncSecKey:
    def __init__(self):
        self.txt = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        self.i = ''.join(random.sample(self.txt, 16))  # 16为随机数
        self.first_key = '0CoJUm6Qyw8W8jud'
    def get(self, song):
        '''
        获取加密的参数
        params是两次加密的
        :param song:
        :return:
        '''
        res = self.get_params(song, self.first_key)
        params = self.get_params(res, self.i)
        encSecKey = self.get_encSecKey()
        return {
            'params': params,
            'encSecKey': encSecKey
        }
    def get_params(self, data, key):
        '''
        获得params,加密字符长度要是16的倍数
        :param data:
        :param key:
        :return:
        '''
        iv = '0102030405060708'
        num = 16 - len(data) % 16
        data = data + num * chr(num)  # 补足
        cipher = AES.new(key.encode(), AES.MODE_CBC, iv.encode())
        result = cipher.encrypt(data.encode())
        result_str = base64.b64encode(result).decode('utf-8')
        return result_str
    def get_encSecKey(self):
        '''
        获取encSecKey，256个字符串
        hexlify--->转换为btyes类型
        pow--->两个参数是幂,三个参数是先幂在取余
        format(rs, 'x').zfill(256)-->256位的16进制
        :return:
        '''
        enc_key = '010001'
        modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        rs = pow(int(hexlify(self.i[::-1].encode('utf-8')), 16), int(enc_key, 16), int(modulus, 16))
        return format(rs, 'x').zfill(256)
def music():
    file_path="data/music.wav"
    # 百度需要的参数
    APP_ID = '31748890'
    API_KEY = 'INDF9ODyUhLg371ySlTSwyBZ'
    SECRET_KEY = 'XAxq2OOgDNFFtDc2weFCAtrwVXA1iorG'
    # 先调用录音函数
    record(file_path)
    # 语音转成文字的内容
    song_message = voice2text(APP_ID, API_KEY, SECRET_KEY, file_path)
    print(song_message)
    input2=''.join(song_message)  #转换成字符串
    song_name=input2[2:]
    Msuic = GetMusic()
    Msuic.get_music_list_info(song_name)
    songid=str(SongId)
    url = 'https://music.163.com/song/media/outer/url?id='+songid
    headers = { 'User-agent':
                'Mozilla/5.0 (X11; Linux x86_64; rv:57.0)Gecko/20100101 Firefox/57.0',
                'Host':'music.163.com',
                'Referer':'https://music.163.com'}
    req = requests.get(url, headers=headers, allow_redirects=False) #拒绝默认的301/302重定向
    musicLink = req.headers['Location']    #从而可以通过html.headers[‘Location’]拿到重定向的URL。
    urllib.request.urlretrieve(musicLink,'data/'+SongName+".mp3")  #下载并重命名文件
    engine = pyttsx3.init()
    engine.say("即将为您播放 "+Songer+' 的 '+SongName)
    engine.runAndWait()
    pygame.mixer.init()
    filename = 'data/' + SongName+'.mp3'
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
#天气播报
def weather():
    # 存放的文件名称
    file_path='data/weather-audio.wav'
    # 百度需要的参数
    APP_ID = '31748890'
    API_KEY = 'INDF9ODyUhLg371ySlTSwyBZ'
    SECRET_KEY = 'XAxq2OOgDNFFtDc2weFCAtrwVXA1iorG'
    # 图灵需要的参数
    TULING_KEY = '466f8cd5ac1146d39b9a0c8c9f857b0f'
    # 先调用录音函数
    record(file_path)
    # 语音转成文字的内容
    weather_message = voice2text(APP_ID, API_KEY, SECRET_KEY, file_path)
    print(weather_message)
    # 抓取中国天气网指定城主天气
    # input_message=['播放重庆天气情况']
    input2 = ''.join(weather_message) # 转换成字符串
    city_name = input2[2:4]
    url = 'https://yiketianqi.com/api'
    params = {
        'appid': '74636861',
        'appsecret': 'tU2SZs6n',
        'version': 'v61',
        'city': city_name
    }
    response = request('GET', url, params=params)
    r = response.json()
    print(r)
    date = r['date']
    week = r['week']
    update_time=r['update_time']
    city = r['city']
    wea = r['wea']
    tem =r['tem']
    tem1 = r['tem1']
    tem2 =r['tem2']
    air_tip=r['air_tips']
    wea = '你好，今天是%s%s，现在北京时间%s，%s天气 %s，气温%s摄氏度~%s摄氏度，现在为%s摄氏度，%s' % (
    date, week, update_time, city, wea, tem1, tem2, tem, air_tip)
    print(wea)
    engine = pyttsx3.init()
    engine.say('即将为您播放' + city_name + "天气情况")
    engine.say(wea)
    engine.runAndWait()
#新闻播报

from requests import request
def news():
    uri = f'http://tempnews.swu.edu.cn/seeyon/xndxNewsData.do?method=getNewwebNewsKdList&startIndex=0&pageSize={10}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/72.0.3626.109 Safari/537.36'}
    response = request(method='GET', url=uri, params={}, headers=headers)
    text = response.text
    html = etree.HTML(text)
    result = html.xpath('//li')
    result = list(map(lambda x: x.xpath('//a/text()'), result))
    result = result[0]
    #return result
    #result = get_news()
    print('\n'.join(result))
    engine = pyttsx3.init()
    engine.say('即将为您播放新闻')
    engine.runAndWait()
    for i in range(1,10+1):   # 取前10条新闻作为例子播放
        s2='%d, '%(i)+result[i-1]
        #print(s2)
        engine.say(s2)  # 播放
        engine.runAndWait()
#GUI界面
import os
import wx
import pyttsx3
import requests
from bs4 import BeautifulSoup
import chardet
from lxml import etree
import urllib
import pygame
import win32com.client
speaker = win32com.client.Dispatch("SAPI.SpVoice")
class Panel1(wx.Panel):
    """class Panel1 creates a panel with an image on it, inherits wx.Panel"""
    def __init__(self, parent, id):
        # create the panel
        wx.Panel.__init__(self, parent,id)
        try:
            image_file = 'bg.png'
            bmp1 = wx.Image(image_file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            self.bitmap1 = wx.StaticBitmap(self, -1, bmp1, (0, 0))
        except IOError:
            print ("Image file is not found") % imageFile
            raise SystemExit
        pic1 = wx.Image("hudong.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        pic2 = wx.Image("yinyue.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        pic3 = wx.Image("tianqiqing.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        pic4 = wx.Image("xinwen.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()

        #绘图按钮1，默认风格3D
        self.button1 = wx.BitmapButton(self.bitmap1, -1, pic1, pos = (230, 420),style=0,size=(50,50))
        self.Bind(wx.EVT_BUTTON, self.On1Click, self.button1)
        self.button1.SetDefault()
        #绘图按钮2，默认风格3D
        self.button2 = wx.BitmapButton(self.bitmap1, -1, pic2, pos = (300, 420),style=0,size=(50,50))
        self.Bind(wx.EVT_BUTTON, self.On2Click, self.button2)
        self.button2.SetDefault()
        #绘图按钮3，默认风格3D
        self.button3 = wx.BitmapButton(self.bitmap1, -1, pic3, pos = (230, 480),style=0,size=(50,50))
        self.Bind(wx.EVT_BUTTON, self.On3Click, self.button3)
        self.button3.SetDefault()
        #绘图按钮4，默认风格3D
        self.button4 = wx.BitmapButton(self.bitmap1, -1, pic4, pos = (300, 480),style=0,size=(50,50))
        self.Bind(wx.EVT_BUTTON, self.On4Click, self.button4)
        self.button4.SetDefault()

    def On1Click(self, event):
        print("人机交互")
        speaker.Speak("您已选择人机交互模式 ")
        chatwithrobot()
        event.Skip()
    def On2Click(self, event):
        print("音乐播放")
        speaker.Speak("您已选择音乐播放模式 ")
        music()
        event.Skip()
    def On3Click(self, event):
        print("天气播报")
        speaker.Speak("您已选择天气播报模式 ")
        weather()
        event.Skip()
    def On4Click(self, event):
        print("新闻播报")
        speaker.Speak("您已选择新闻播报模式 ")
        news()
        event.Skip()


app = wx.App(False)
frame1 = wx.Frame(None, -1, title='Robot', size=(600, 640))
# create the class instance
panel1 = Panel1(frame1, -1)
frame1.Show(True)
app.MainLoop()

