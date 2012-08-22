# -*- coding: utf8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from records.models import Record

@login_required
def index(request):
    return render(request, 'pages/index.html', {})

def login(request):
    try:
        next = request.GET['next']
    except KeyError:
        next = '/'

    return render(request, 'pages/login.html', {'next': next})

@permission_required("records.submit_records")
def submit_record(request):
    try:
        rid = request.GET['rid']
    except KeyError:
        rid = None

    if rid:
        record = Record.objects.get(id=rid)
    else:
        record = None

    if record:
        tonn = record.players.get(kaze="동")
        nann = record.players.get(kaze="남")
        sha = record.players.get(kaze="서")
        pei = record.players.get(kaze="북")

        players = {
            "tonn": tonn,
            "nann": nann,
            "sha": sha,
            "pei": pei
        }
    else:
        players = None

    return render(request, 'pages/submit_record.html', {'record': record, 'players': players})
