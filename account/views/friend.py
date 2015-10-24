# -*- coding: utf-8 -*-
from django.contrib.auth.models import User

from rest_framework.decorators import api_view
from rest_framework.response import Response

from couple.models import RandomMath
from account.serializers import UserInfoSerializer

def random_match_user(user, gender):
    'random create RandomMath by gender'
    random_users = User.objects.filter(userinfo__gender=gender).order_by('?')[0:10]
    if gender == '0':
        for random_user in random_users:
            try:
                RandomMath.objects.create(boy=random_user,girl=user)
            except RandomMath.IntegrityError:
                pass
        return RandomMath.objects.filter(girl=user).order_by('-vote')[0:10]
    else:
        for random_user in random_users:
            try:
                RandomMath.objects.create(boy=user,girl=random_user)
            except RandomMath.IntegrityError:
                pass
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


