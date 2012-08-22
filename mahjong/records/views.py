# -*- coding: utf8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from django.http import Http404, HttpResponseRedirect, HttpResponse
from records.models import Record, Player

def get_user_from_name(name):
    try:
        user = User.objects.get(username=name)
    except ObjectDoesNotExist:
        try:
            user = User.objects.get(first_name=name)
        except ObjectDoesNotExist:
            user = None
    return user

@permission_required("records.submit_records")
def submit_record_proc(request):
    try:
        tonn_username = request.POST['tonn_username']
        nann_username = request.POST['nann_username']
        sha_username = request.POST['sha_username']
        pei_username = request.POST['pei_username']
        tonn_score = int(request.POST['tonn_score'])
        nann_score = int(request.POST['nann_score'])
        sha_score = int(request.POST['sha_score'])
        pei_score = int(request.POST['pei_score'])
        match_type = int(request.POST['match_type'])
    except KeyError:
        raise Http404

    try:
        extra_point = int(request.POST['extra_point'])
    except KeyError:
        extra_point = 0

    # validate point inputs
    total = tonn_score + nann_score + sha_score + pei_score + extra_point
    if total % 10000 or total % 4:
        return HttpResponse("Invalid points...");

    # create record
    record = Record(extra_point=extra_point, match_type=match_type)
    record.save()

    # get users
    tonn = get_user_from_name(tonn_username)
    nann = get_user_from_name(nann_username)
    sha = get_user_from_name(sha_username)
    pei = get_user_from_name(pei_username)

    if not tonn or not nann or not sha or not pei:
        return HttpResponse("Invalid users...");

    # create player
    tonn_player = Player(user=tonn, record=record, kaze="동", point=tonn_point)
    tonn_player.save()
    nann_player = Player(user=nann, record=record, kaze="남", point=nann_point)
    nann_player.save()
    sha_player = Player(user=sha, record=record, kaze="서", point=sha_point)
    sha_player.save()
    pei_player = Player(user=pei, record=record, kaze="북", point=pei_point)
    pei_player.save()

    return HttpResponseRedirect("/submit_record")

@permission_required("records.submit_records")
def modify_record_proc(request):
    try:
        rid = request.POST['rid']
        tonn_username = request.POST['tonn_username']
        nann_username = request.POST['nann_username']
        sha_username = request.POST['sha_username']
        pei_username = request.POST['pei_username']
        tonn_score = int(request.POST['tonn_score'])
        nann_score = int(request.POST['nann_score'])
        sha_score = int(request.POST['sha_score'])
        pei_score = int(request.POST['pei_score'])
        match_type = int(request.POST['match_type'])
    except KeyError:
        raise Http404

    try:
        extra_point = int(request.POST['extra_point'])
    except KeyError:
        extra_point = 0

    # validate point inputs
    total = tonn_score + nann_score + sha_score + pei_score + extra_point
    if total % 10000 or total % 4:
        return HttpResponse("Invalid points...");

    # create record
    record = Record.objects.get(id=rid)
    record.extra_point = extra_point
    record.match_type = match_type
    record.save()

    # get users
    tonn = get_user_from_name(tonn_username)
    nann = get_user_from_name(nann_username)
    sha = get_user_from_name(sha_username)
    pei = get_user_from_name(pei_username)

    if not tonn or not nann or not sha or not pei:
        return HttpResponse("Invalid users...");

    # empty users
    Player.objects.filter(record=record).delete()

    # create player
    tonn_player = Player(user=tonn, record=record, kaze="동", point=tonn_point)
    tonn_player.save()
    nann_player = Player(user=nann, record=record, kaze="남", point=nann_point)
    nann_player.save()
    sha_player = Player(user=sha, record=record, kaze="서", point=sha_point)
    sha_player.save()
    pei_player = Player(user=pei, record=record, kaze="북", point=pei_point)
    pei_player.save()

    return HttpResponseRedirect("/submit_record?rid="+rid)
