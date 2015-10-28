# -*- coding: utf-8 -*-
from rest_framework.decorators import api_view
from rest_framework.response import Response

from account.serializers import UserInfoSerializer
from account.models import UserInfo, PhoneFriend

from couple.models import RandomMath

@api_view(['GET'])
def random_list(request):
    user = request.user

    try:
        phone_friends = PhoneFriend.objects.filter(user=user).order_by('?').all()
    except:
        phone_friends = []

    boys  = []
    girls = []
    for phone_friend in phone_friends:
        if phone_friend.friend.userinfo.gender == '0':
            if len(boys) < 5:
                boys.append(phone_friend.friend.userinfo)
        else:
            if len(girls) < 5:
                girls.append(phone_friend.friend.userinfo)

    add_boy_count = 5 - len(boys)
    add_girl_count = 5 - len(girls)

    if add_boy_count > 0:
        add_boys = UserInfo.objects.filter(gender='0').order_by('?')[:add_boy_count]
        boys.extend(add_boys)
    
    if add_girl_count > 0:
        add_girls = UserInfo.objects.filter(gender='1').order_by('?')[:add_girl_count]   # random fetch 5 girls
        girls.extend(add_girls)

    boys_serializer = UserInfoSerializer(boys, fields=('user', 'avatar'), many=True)
    girls_serializer = UserInfoSerializer(girls, fields=('user', 'avatar'), many=True)
    
    return Response({
        'result': 1,
        'boys': boys_serializer.data,
        'girls': girls_serializer.data,
        })

@api_view(['POST'])
def random_match(request):
    receive = request.data
    boy_id  = receive.get('boy', None)
    girl_id = receive.get('girl', None)
    try: 
        UserInfo.objects.get(user_id=boy_id, gender='0')
        UserInfo.objects.get(user_id=girl_id, gender='1')
    except UserInfo.DoesNotExist:
        return Response({
            'result': 0,
            'cause': u'某用户不存在或性别错误',
            }) 
    
    random_match = RandomMath.objects.filter(boy_id=boy_id, girl_id=girl_id).all()[0:1]

    if not random_match:
        random_match = RandomMath(boy_id=boy_id, girl_id=girl_id)
        random_match.save()
    else:
        random_match = random_match[0]
        vote = random_match.vote
        vote += 1
        random_match.vote = vote
        random_match.save()

    return Response({
        'result': 1,
        'vote': random_match.vote,
        })

# @api_view(['GET'])
# def random_match_rank_list(request):
#     random_list = RandomMath.objects.order_by('-vote').all()[0:10]
#     random_list_serializer = RandomMathSerializer(random_list, many=True)
#     for i, item in enumerate(random_list_serializer.data):
#         random_list_one = random_list[i]
#         item['boy_avatar'] = random_list_one.boy.userinfo.avatar.url
#         item['girl_avatar'] = random_list_one.girl.

#     return Response({
#         'result': 1,
#         'rank_list': love_show_list_serializer.data,
#         })