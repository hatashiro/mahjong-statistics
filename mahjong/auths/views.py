# -*- coding: utf8 -*-
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from mahjong.settings import SQLITE3_PATH, SQLITE3_BACKUP_PATH

from datetime import datetime

import shutil, os

def login_proc(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
    except KeyError:
        raise Http404

    try:
        next = request.POST['next']
    except KeyError:
        next = '/'

    user = authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            login(request, user)

            # redirect
            return HttpResponseRedirect(next)
        else:
            raise Http404
    else:
        raise Http404

def logout_proc(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def changepasswd_proc(request):
    try:
        passwd = request.POST['passwd']
    except KeyError:
        raise Http404

    request.user.set_password(passwd)
    request.user.save()

    return HttpResponseRedirect('/change_passwd')

def xml_users(request):
    users = User.objects.all()
    return render(request, 'xml/users.xml', {"users": users})

@login_required
def backupdb_proc(request):
    if not request.user.is_staff:
        raise Http404

    try:
        os.mkdir(SQLITE3_BACKUP_PATH)
    except OSError:
        pass

    shutil.copyfile(SQLITE3_PATH, os.path.join(SQLITE3_BACKUP_PATH, 'mahjong-sqlite3-backup-' + datetime.now().strftime('%Y%m%d%H%M%S')))

    return HttpResponse('Database backuped')
