# -*- coding: utf-8 -*-
from rest_framework.decorators import api_view
from rest_framework.response import Response

from couple.models import RandomMath
from account.serializers import UserInfoSerializer

@api_view(['GET'])
def match_user_list(request):
    user = request.user
    if user.userinfo.gender == '1':
        random_matchs = RandomMath.objects.filter(girl=user).order_by('vote')[0:5]
        boys_info = [random_match.boy.userinfo for random_match in random_matchs]
        info_serializer = UserInfoSerializer(boys_info, many=True)
    else:
        random_matchs = RandomMath.objects.filter(boy=user).order_by('vote')[0:5]
        girls_info = [random_match.girl.userinfo for random_match in random_matchs]
        info_serializer = UserInfoSerializer(girls_info, many=True)

    return Response({
        'result': 1,
        'match_users': info_serializer.data,
        })

        