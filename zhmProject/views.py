# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from zhmProject.models import Event, Guest


# Create your views here.
def index(request):
    # return HttpResponse("Hello Django!")
    return render(request, "index.html")


def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            # if username == 'admin' and password =='admin':
            # return HttpResponse(u'登录成功')
            # return HttpResponseRedirect('/event_manage/')
            # response = HttpResponseRedirect('/event_manage/')   # 添加浏览器cookie
            # response.set_cookie('user',username,3600)
            # return response
            request.session['user'] = username
            response = HttpResponseRedirect('/event_manage/')
            return response
        else:
            return render(request, 'index.html', {'error': u'用户名或密码错误！'})


@login_required
def event_manage(request):
    # username = request.COOKIES.get('user','') #读取浏览器cookie
    event_list = Event.objects.all()
    username = request.session.get('user', '')

    return render(request, "event_manage.html", {"user": username, "events": event_list})


@login_required
def search_name(request):
    username = request.session.get('user', '')
    search_name = request.GET.get("name", "")
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request, "event_manage.html", {"user": username, "events": event_list})


@login_required
def guest_manage(request):
    username = request.session.get('user', '')
    guest_list = Guest.objects.all()
    paginator = Paginator(guest_list,2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request, "guest_manage.html", {"user": username, "guests": contacts})


@login_required
def search_phone(request):
    username = request.seesion.get('user', '')
    search_phone = request.GET.get("phone", "")
    guest_list = Guest.objects.filter(phone__contains=search_phone)
    return render(request, "guest_manage.html", {"user": username, "guests": guest_list})
# 退出登录
@login_required
def logout(request):
    auth.logout(request)  # 退出登录
    response = HttpResponseRedirect('/index/')
    return response