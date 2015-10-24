# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.contrib import auth

from rest_framework.decorators import api_view
from rest_framework.response import Response


from account.forms import RegisterForm
from account.models import Token, UserInfo
from account.serializers import UserInfoSerializer
from account.forms import SettingPasswordForm

from couple.models import LoveShow


from match.settings import app_key, master_secret

import base64
import requests
import json

@api_view(['POST'])
def register(request):
    recevie = request.data
    gender = recevie.get('gender', '0')
    form = RegisterForm(recevie)
    if not form.is_valid():
        return Response({
            'result': 0,
            'cause': form.errors,
            })

    print request.FILES
    avatar = request.FILES.get('avatar', None)
    if not avatar:
        return Response({
            'result': 0,
            'cause': u'必须上传头像'
            })

    ##### "注册到极光即时聊天" ######   
    JIM = 'https://api.im.jpush.cn/v1/users/'
    data = [{"username": form.cleaned_data['username'], "password": form.cleaned_data['password']},]
    data = json.dumps(data)
    base64_auth_string = base64.b64encode(app_key + ':' + master_secret)
    headers = dict()
    headers['Authorization'] = 'Basic ' + base64_auth_string
    headers["Content-type"] = "application/json;charset:utf-8"
    response = requests.post(JIM, data=data, headers=headers, verify=False)
    if  response.status_code != 201:
        return Response({
            "result": 0,
            "cause": u"注册失败",
            })
    ############
    new_user = form.save()


    user_info = UserInfo.objects.create(user=new_user, nickname=form.cleaned_data['username'], gender=gender, avatar=avatar)
    token = Token.objects.create(user=new_user)

    serializer = UserInfoSerializer(user_info)
    response = serializer.data             
    response['token'] = token.key

    return Response({
        'result': 1,
        'user_info': response
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

        try:
            love_show = LoveShow.objects.get(user=user)
            response['lover'] = love_show.lover.url
        except LoveShow.DoesNotExist:
            response['lover'] = ''

        return Response({
            "result": 1,
            "user_info": response,
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

@api_view(['GET'])
def check_user(request):
    receive = request.GET
    check_username = receive.get('check_username', None)
    
    if check_username:
        try:
            user = User.objects.get(username=check_username)
        except User.DoesNotExist:
            return Response({
                'result': 0,
                'cause': u'用户不存在'
                })

        return Response({
            'result': 1,
            'avatar': user.userinfo.avatar.url,
            'nickname': user.userinfo.nickname
            })
    else:
        return Response({
            'result': 0,
            'cause': u'未指定用户'
            })

@api_view(['POST'])
def settings(request):
    user = request.user
    receive = request.data    
    change_nickname = receive.get('nickname', None)
    change_gender = receive.get('gender', None)
    change_password = receive.get('password', None)
    change_avatar = request.FILES.get('avatar', None)

    if change_avatar:
        UserInfo.objects.filter(user=user).update(avatar=change_avatar)
    
    if change_password:
        form = SettingPasswordForm(request)
        if not form.is_valid():
            return Response({
                'result': 0,
                'cause': form.errors
                })

    if change_nickname:
        UserInfo.objects.filter(user=user).update(nickname=change_nickname)
    
    if change_gender and change_gender in ['0', '1']:
        UserInfo.objects.filter(user=user).update(gender=change_gender)
    
    return Response({
        'result': 1,
        })



