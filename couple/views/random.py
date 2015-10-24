# -*- coding: utf-8 -*-
from rest_framework.decorators import api_view
from rest_framework.response import Response

from account.serializers import UserInfoSerializer
from account.models import UserInfo

from couple.models import RandomMath

@api_view(['GET'])
def random_list(request):
    boys = UserInfo.objects.filter(gender='0').order_by('?')[:5]    # random fetch 5 boys
    girls = UserInfo.objects.filter(gender='1').order_by('?')[:5]   # random fetch 5 girls
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



