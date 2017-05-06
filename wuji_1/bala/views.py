from django.shortcuts import render
from django.http import HttpResponse
import json
from .script import Youtube
def index(request):
    return render(request,'youtube.html')
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
    #Youtube.main(url)
    return HttpResponse(json.dumps(data), content_type="application/json")

# Create your views here.
