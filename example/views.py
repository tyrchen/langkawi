from django.shortcuts import render_to_response
from django.template import RequestContext
from langkawi.contrib.weibo.client import Weibo
from pprint import pprint

def home(request):
    #content = RequestContext(request, {'content': 'social text'})
    content = {}
    return render_to_response('home.html',  content, context_instance=RequestContext(request))

def profile(request):
    return render_to_response('profile.html',{})

def upload(request):
    if request.method == 'POST':
        text = request.POST['text']
        f = handle_uploaded_file(request.FILES['pic'])
        client = Weibo()
        client = request.session[client.get_session_key()]
        response = client.send(text, f.name)
        pprint(response.request.headers)
        pprint(response.request.data)
    return render_to_response('upload.html', {'file':f, 'text':text, 'response':response.text})

def handle_uploaded_file(f):
    with open(f.name, 'wb+') as info:
        for chunk in f.chunks():
            info.write(chunk)
    return f
