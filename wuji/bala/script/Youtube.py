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
#url=u'https://www.youtube.com/results?search_query=AOA+fancam'
class Youtube():
    def __init__(self):
        self.download_path='/Users/wujishanxia/Downloads'
    def youtube_download(self,url,id):
        #download_command=['youtube-dl -f bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio\
        #                  --merge-output-format mp4 -o /Users/wujishanxia/Downloads/test.mp4',url]
        command='youtube-dl'+' -f bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'+' -o'+' '+str(id)+'.mp4'+' '+url
        #thread=threading.Thread(target=self.download,args=(command,id))
        #thread.setDaemon(True)
        #thread.start()
        download=subprocess.Popen(command,shell=True)
        #download = subprocess.Popen('echo "hello"',shell=True)
        download.wait()
        #with youtube_dl.YoutubeDL() as ydl:
        #    ydl.download(['http://www.bilibili.com/video/av2331280?from=search&seid=831467570734192523'])
        print 'download video successfully'
        gif_command='ffmpeg -ss 20 -t 20 -i'+' '+str(id)+'.mp4  -s 320x240 -f gif'+' '+str(id)+'.gif'
        gif=subprocess.Popen(gif_command,shell=True)
        gif.wait()
        print 'generate gif successfully'
        cp_command='cp'+' '+str(id)+'.gif'+' /home/www/public/media'
        cp = subprocess.Popen(cp_command, shell=True)
        cp.wait()
        print 'copy gif to media successfully'
        rm_command='rm'+' '+str(id)+'.mp4'
        rm = subprocess.Popen(rm_command,shell=True)
        rm.wait()
        print 'rm mp4 successfully'
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
        videos=soup.select('h3[class="yt-lockup-title "] > a')
        #print len(videos)
        #for video in videos:
            #return 'https://www.youtube.com'+video['href']
        return videos
class VideoToImagine():
    pass
def main(url):
    spider=Spider()
    youtube=Youtube()
    html=spider.get_html(url)
    #print html
    #html=open('/Users/wujishanxia/Documents/YouTube.html','r').read()
    #print html
    videos=spider.get_video_url(html)
    #print video_url
    download_thread_list = []  # 线程存放列表
    for i in xrange(4):
        video_url = 'https://www.youtube.com' + videos[i]['href']
        t = threading.Thread(target=youtube.youtube_download, args=(video_url,i))
        #t.setDaemon(True)
        download_thread_list.append(t)
    for t in download_thread_list:
        t.start()
    for t in download_thread_list:
        t.join()