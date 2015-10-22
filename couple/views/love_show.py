# -*- coding: utf-8 -*-
from django.contrib.auth.models import User

from rest_framework.decorators import api_view
from rest_framework.response import Response

from account.serializers import UserInfoSerializer
from account.models import UserInfo

from couple.models import LoveShow

@api_view(['GET'])
def lovers_get(request):
    love_shows = LoveShow.objects.order_by('?')[0:10]
    lovers = []

    for love_show in love_shows:
        item = dict([])
        item['id'] = love_show.id
        if love_show.user.userinfo.gender == '0':
            item['boy_avatar'] = love_show.user.userinfo.avatar.mid_url
            item['girl_avatar'] = love_show.lover.mid_url
        else:
            item['girl_avatar'] = love_show.user.userinfo.avatar.mid_url
            item['boy_avatar'] = love_show.lover.mid_url
        lovers.append(item)

    return Response({
        'result': 1,
        'lovers': lovers
        })

@api_view(['POST'])
def lovers_favour_or_oppose(request):
    love_show_id = int(request.data.get('love_show_id'))
    judge = int(request.data.get('judge', '1'))
    try:
        love_show = LoveShow.objects.get(id=love_show_id)
    except LoveShow.DoesNotExist:
        return Response({
            'result': 0,
            'cause': u'指定恩爱狗不存在',
            })

    if judge == 1:
        favour = love_show.favour
        favour += 1
        LoveShow.objects.filter(id=love_show_id).update(favour=favour)

    elif judge == 0:
        oppose = love_show.oppose
        oppose += 1
        LoveShow.objects.filter(id=love_show_id).update(oppose=oppose)

    else:
        return Response({
            'result': 0,
            'cause': u'请选择点赞或踩一脚',
            })

    return Response({
        'result': 1,
        })