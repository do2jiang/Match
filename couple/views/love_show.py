# -*- coding: utf-8 -*-
from rest_framework.decorators import api_view
from rest_framework.response import Response

from account.serializers import LoveShowSerializer

from couple.models import LoveShow

@api_view(['GET'])
def lovers_get(request):
    love_shows = LoveShow.objects.order_by('?')[0:10]
    lovers = []

    for love_show in love_shows:
        item = dict([])
        item['id'] = love_show.id
        if love_show.user.userinfo.gender == '0':
            item['boy_avatar'] = love_show.user.userinfo.avatar.url
            item['girl_avatar'] = love_show.lover.url
        else:
            item['girl_avatar'] = love_show.user.userinfo.avatar.url
            item['boy_avatar'] = love_show.lover.url
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

@api_view(['GET'])
def lover_rank_list(request):
    user = request.user
    my_show = LoveShow.objects.get(user=user)
    my_favour = my_show.favour
    rank = LoveShow.objects.filter(favour__lt=my_favour).count()
    my_show_serializer = dict([])
    my_show_serializer['avatar'] = user.userinfo.avatar.url
    my_show_serializer['lover'] = my_show.lover.url
    my_show_serializer['favour'] = my_favour
    my_show_serializer['rank'] = rank + 1


    love_show_list = LoveShow.objects.order_by('-favour').all()[0:10]
    love_show_list_serializer = LoveShowSerializer(love_show_list, many=True)
    for i, item in enumerate(love_show_list_serializer.data):
        love_show_list_one = love_show_list[i]
        item['avatar'] = love_show_list_one.user.userinfo.avatar.url

    return Response({
        'result': 1,
        'my_lover': my_show_serializer,
        'rank_list': love_show_list_serializer.data,
        })



@api_view(['GET'])
def love_show_hot_list(request):
    love_show_list = LoveShow.objects.order_by('-hot').all()[0:10]
    love_show_list_serializer = LoveShowSerializer(love_show_list, many=True)
    for i, item in enumerate(love_show_list_serializer.data):
        love_show_list_one = love_show_list[i]
        item['avatar'] = love_show_list_one.user.userinfo.avatar.url

    return Response({
        'result': 1,
        'rank_list': love_show_list_serializer.data,
        })
