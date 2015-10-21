# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db.models import F

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
    matchs = receive.get('matchs', None)
    if matchs:
        vote_count = []
        for match in matchs:
            boy_id  = match.get('boy', None)
            girl_id = match.get('girl', None)
            try: 
                boy = UserInfo.objects.get(user_id=boy_id, gender=0)
                girl = UserInfo.objects.get(user_id=girl_id, gender=1)
            except UserInfo.DoesNotExist:
                return Response({
                    'result': 0,
                    'cause': u'某用户不存在或性别错误',
                    }) 
            
            try:
                random_match = RandomMath.objects.get(boy_id=boy_id, girl_id=girl_id)
                # random_match.vote = F('vote') + 1
                # random_match.save()
                random_match.vote += 1
                random_match.save()
            except RandomMath.DoesNotExist:
                random_match = RandomMath(boy_id=boy_id, girl_id=girl_id)
                random_match.save()
        
            vote_count.append(random_match.vote)
            
        return Response({
            'result': 1,
            'vote': vote_count,
            })



