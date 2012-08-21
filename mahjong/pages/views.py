# -*- coding: utf8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return render(request, 'pages/index.html', {})

def login(request):
    try:
        next = request.GET['next']
    except KeyError:
        next = '/'

    return render(request, 'pages/login.html', {'next': next})
