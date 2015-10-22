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
        if love_show.user.userinfo.gender == '0':
            item['boy_avatar'] = love_show.user.userinfo.avatar.thumb_url
            item['girl_avatar'] = love_show.lover.thumb_url
        else:
            item['girl_avatar'] = love_show.user.userinfo.avatar.thumb_url
            item['boy_avatar'] = love_show.lover.thumb_url
        lovers.append(item)
    return Response({
        'result': 1,
        'lovers': lovers
        })

