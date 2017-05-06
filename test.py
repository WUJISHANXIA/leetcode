#! /usr/bin/env python
# -*- coding: utf-8 -*-
import youtube_dl
#import cv2
import requests
from bs4 import BeautifulSoup
import youtube_dl
import sys,subprocess
import threading
#url=u'https://www.youtube.com/user/spinelcam/videos'
url=u'http://search.bilibili.com/all?keyword=AOA金雪炫&from_source=banner_search'
class Youtube():
    def __init__(self):
        self.download_path='/Users/wujishanxia/Downloads'
    def download(self):
        #download=subprocess.Popen('youtube-dl http://www.bilibili.com/video/av2331280?from=search&seid=10132791050288117155',shell=True)
        #download = subprocess.Popen('echo "hello"',shell=True)
        #download.wait()
        with youtube_dl.YoutubeDL() as ydl:
            ydl.download(['http://www.bilibili.com/video/av2331280?from=search&seid=831467570734192523'])
        print '2'
    def youtube_download(self,url):
        #download_command=['youtube-dl -f bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio\
        #                  --merge-output-format mp4 -o /Users/wujishanxia/Downloads/test.mp4',url]
        command='youtube-dl http://www.bilibili.com/video/av2331280?from=search&seid=10132791050288117155'
        print 'haha'
        thread=threading.Thread(target=self.download,args=[])
        #thread.setDaemon(True)
        thread.start()
class Spider():
    def __init__(self):
        self.header={

            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept':'*/*',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
        }
    def get_html(self,url):
        s=requests.session()
        s.headers.update(self.header)
        response=s.get(url)
        return response.content
    def get_video_url(self,html):
        soup=BeautifulSoup(html,"html.parser")
        videos=soup.select('a[lnk-type="video"]')
        for video in videos:
            return 'http:'+video['href']
            break
class VideoToImagine():
    pass
if __name__=='__main__':
    youtube=Youtube()
    youtube.youtube_download('http://www.bilibili.com/video/av2331280?from=search&seid=14191289368909661658')

