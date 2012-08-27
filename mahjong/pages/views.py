# -*- coding: utf8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from records.models import Record
from records.stat import Stat

from datetime import datetime

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
        tonn = record.player_set.get(kaze="동")
        nann = record.player_set.get(kaze="남")
        sha = record.player_set.get(kaze="서")
        pei = record.player_set.get(kaze="북")

        players = {
            "tonn": tonn,
            "nann": nann,
            "sha": sha,
            "pei": pei
        }
    else:
        players = None

    return render(request, 'pages/submit_record.html', {'record': record, 'players': players})

def filter_with_month(queryset, year, month):
    to_year = year
    to_month = month + 1
    if to_month > 12:
        to_month -= 12
        to_year += 1

    return queryset.filter(uploaded__gte=datetime(year, month, 1), uploaded__lt=datetime(to_year, to_month, 1))

@login_required
def records(request):
    try:
        year = request.GET['year']
        if year == 'all':
            entire = True
        else:
            year = int(year)
            month = int(request.GET['month'])
            entire = False
    except:
        entire = False
        year = datetime.now().year
        month = datetime.now().month

    # get date range
    date_range = {}
    try:
        date_oldest = Record.objects.filter(valid=True).order_by('uploaded')[0].uploaded
    except:
        date_oldest = datetime.now()

    for _year in range(datetime.now().year, date_oldest.year-1, -1):
        date_range[_year] = []
        for _month in range(12, 0, -1):
            if _year == date_oldest.year and _month < date_oldest.month:
                continue
            if _year == datetime.now().year and _month > datetime.now().month:
                continue
            if filter_with_month(Record.objects.filter(valid=True), _year, _month).count() == 0:
                continue
            date_range[_year].append(_month)

    if entire:
        records = Record.objects.filter(valid=True)
    else:
        records = filter_with_month(Record.objects.filter(valid=True), year, month)

    return render(request, 'pages/records.html', {'date_range': date_range, 'records': records})

@login_required
def stats(request):
    try:
        year = request.GET['year']
        if year == 'all':
            entire = True
        else:
            year = int(year)
            month = int(request.GET['month'])
            entire = False
    except:
        entire = False
        year = datetime.now().year
        month = datetime.now().month

    # get date range
    date_range = {}
    try:
        date_oldest = Record.objects.filter(valid=True).order_by('uploaded')[0].uploaded
    except:
        date_oldest = datetime.now()

    for _year in range(datetime.now().year, date_oldest.year-1, -1):
        date_range[_year] = []
        for _month in range(12, 0, -1):
            if _year == date_oldest.year and _month < date_oldest.month:
                continue
            if _year == datetime.now().year and _month > datetime.now().month:
                continue
            if filter_with_month(Record.objects.filter(valid=True), _year, _month).count() == 0:
                continue
            date_range[_year].append(_month)

    stats = []
    for user in User.objects.all():
        if entire:
            stat = Stat(user)
        else:
            stat = Stat(user, year, month)

        if stat.valid:
            stats.append(stat)

    # order by winpoint
    stats = sorted(stats, key=lambda stat: stat.winpoint)

    return render(request, 'pages/stats.html', {'date_range': date_range, 'stats': stats})

@login_required
def change_passwd(request):
    return render(request, 'pages/change_passwd.html', {})
