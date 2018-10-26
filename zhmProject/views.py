# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from  django.contrib.auth.decorators import login_required
from zhmProject.models import Event
# Create your views here.
def index(request):
    #return HttpResponse("Hello Django!")
    return render(request,"index.html")
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
        #if username == 'admin' and password =='admin':
           # return HttpResponse(u'登录成功')
           # return HttpResponseRedirect('/event_manage/')
           # response = HttpResponseRedirect('/event_manage/')   # 添加浏览器cookie
           # response.set_cookie('user',username,3600)
           # return response
            request.session['user'] = username
            response = HttpResponseRedirect('/event_manage/')
            return response
        else:
            return render(request,'index.html',{'error':u'用户名或密码错误！'})
@login_required
def event_manage(request):
    # username = request.COOKIES.get('user','') #读取浏览器cookie
    event_list = Event.objects.all()
    username = request.session.get('user','')

    return render(request,"event_manage.html",{"user":username,"events":event_list})