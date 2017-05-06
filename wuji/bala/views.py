from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.cache import  cache_control
from django.http import HttpResponseRedirect
import json,random
from .script import Youtube
@cache_control(no_cache=True)
def index(request):
    v=random.random()
    img0_src = 'http://23.83.247.108/media/0.gif' + '?v=' + str(v)
    img1_src = 'http://23.83.247.108/media/1.gif' + '?v=' + str(v)
    img2_src = 'http://23.83.247.108/media/2.gif' + '?v=' + str(v)
    img3_src = 'http://23.83.247.108/media/3.gif' + '?v=' + str(v)
    return render(request,'youtube.html',context={'img0':img0_src,'img1':img1_src,'img2':img2_src,'img3':img3_src})
@cache_control(no_cache=True)
def youtube(request):
    data = {}
    search_url='https://www.youtube.com/results?search_query='
    url=''
    data["url"] = request.GET['url']
    for x in data["url"].split():
        if url:
            url += '+' + x
        else:
            url += x
    #print data
    url=search_url+url
    data["url"]=url
    Youtube.main(url)
    return HttpResponseRedirect('youtube/aoa')
# Create your views here.
