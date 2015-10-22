# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.contrib import auth

from rest_framework.decorators import api_view
from rest_framework.response import Response


from account.forms import RegisterForm
from account.models import Token, UserInfo
from account.serializers import UserInfoSerializer

@api_view(['POST'])
def register(request):
    recevie = request.data
    gender = recevie.get('gender', '0')
    form = RegisterForm(recevie)
    if not form.is_valid():
        return Response({
            'cause': form.errors,
            })

    new_user = form.save()
    avatar = request.FILES.get('avatar', None)
    # if not avatar:
    #     return Response({
    #         'result': 0,
    #         'cause': u'必须上传头像'
    #         })

    UserInfo.objects.create(user=new_user, gender=gender, avatar=avatar)
    Token.objects.create(user=new_user)

    return Response({
        'result': 1,
        # 'token': user.token.key
        })


@api_view(['POST'])
def login(request):
    receive = request.data   
    username = receive['username']
    password = receive['password']
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        # update the token
        try:
            token = Token.objects.get(user=user)  
            token.delete()
        except Token.DoesNotExist:
            pass

        token = Token.objects.create(user=user)
        user_info = UserInfo.objects.get(user=user)
        serializer = UserInfoSerializer(user_info)
        
        response = serializer.data             
        response['token'] = token.key

        return Response({
            "result": 1,
            "user_info": response,
            # response contain user_info and token 
            })
    else:
        try:
            User.objects.get(username=username)
            cause = u'密码错误'
        except User.DoesNotExist:
            cause = u'用户不存在'

        return Response({
            "result": 0,
            "cause":cause,
            #"Token"
            })
