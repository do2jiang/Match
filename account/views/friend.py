# -*- coding: utf-8 -*-
from django.contrib.auth.models import User

from rest_framework.decorators import api_view
from rest_framework.response import Response

from couple.models import RandomMath

from account.serializers import UserInfoSerializer
from account.models import PhoneFriend

@api_view(['POST'])
def get_phone_friends(request):
    print request.data
    user = request.user
    phone_friends = request.data.get('phone_friends', None)
    if phone_friends:
        for phone_friend in phone_friends:
            try:
                friend = User.objects.get(username=phone_friend)
                PhoneFriend.objects.get_or_create(user=user, friend=friend)
            except User.DoesNotExist:
                pass
        return Response({
            'result': 1
            })
    else:
        return Response({
            'result': 0,
            'cause': u'查询通讯录好友失败'
            })


def random_match_user(user, gender):
    'random create RandomMath by gender'
    random_users = User.objects.filter(userinfo__gender=gender).order_by('?')[0:10]
    if gender == '0':
        for random_user in random_users:
            if not RandomMath.objects.filter(boy=random_user,girl=user).exists():
                RandomMath.objects.create(boy=random_user,girl=user)
        return RandomMath.objects.filter(girl=user).order_by('-vote')[0:10]
    else:
        for random_user in random_users:
            if not RandomMath.objects.filter(girl=random_user, boy=user).exists():
                RandomMath.objects.create(girl=random_user, boy=user)
        return RandomMath.objects.filter(boy=user).order_by('-vote')[0:10]
        

@api_view(['GET'])
def match_user_list(request):
    user = request.user
    
    if user.userinfo.gender == '1':
        random_matchs = RandomMath.objects.filter(girl=user).order_by('-vote')[0:10]
        random_match_count = random_matchs.count()
        if  random_match_count < 10:
            random_matchs = random_match_user(user=user, gender='0')
        
        boys_name = [random_match.boy.username for random_match in random_matchs]
        boys_info = [random_match.boy.userinfo for random_match in random_matchs]
        
        info_serializer = UserInfoSerializer(boys_info, fields=('nickname', 'avatar'), many=True)
        for i, item in enumerate(info_serializer.data):
            item['username'] = boys_name[i]


    else:
        random_matchs = RandomMath.objects.filter(boy=user).order_by('-vote')[0:10]
        random_match_count = random_matchs.count()
        if  random_match_count < 10:
            random_matchs = random_match_user(user=user, gender='1')

        girls_name = [random_match.girl.username for random_match in random_matchs]
        girls_info = [random_match.girl.userinfo for random_match in random_matchs]

        info_serializer = UserInfoSerializer(girls_info, fields=('nickname', 'avatar'), many=True)
        # print girls_name
        # print info_serializer.data
        for i, item in enumerate(info_serializer.data):
            item['username'] = girls_name[i]
    
    return Response({
        'result': 1,
        'match_users': info_serializer.data,
        })

@api_view(['POST'])
def link_user(request):
    user = request.user
    if user.userinfo.gender == '1':
        lover_gender = '0'
    else:
        lover_gender = '1'

    link_username = request.data.get('link_username', '')
    try:
        lover = User.objects.get(username=link_username, userinfo__gender=lover_gender)
    except User.DoesNotExist:
        return Response({
            'result': 0,
            'cause': u'用户不存在或性别不符合'
            })

    # send_message to user
    return Response({
        'result': 1,
        })

