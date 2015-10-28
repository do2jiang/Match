#encoding=utf-8
from django.contrib.auth.models import User
from django.contrib import auth

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from account.models import Token, UserInfo
from account.serializers import UserInfoSerializer

from couple.models import LoveShow


from match.settings import app_key, master_secret

import base64
import requests
import json
import re

@api_view(['POST'])
def register(request):
    recevie = request.data
    username = recevie.get('username', '')
    password = recevie.get('password', '')
    gender = recevie.get('gender', '0')

    if not password:
        return Response({
            'result':0,
            'cause':u'请输入密码'
            })

    try:
        User.objects.get(username=username)
        cause = u"用户名已存在"
        print '1'
        return Response({
            'result':0,
            'cause':u"用户名已存在"
            })
    except User.DoesNotExist:
        USER_RE = re.compile(u'^[a-zA-Z0-9_-]{3,20}$')
        if not USER_RE.match(username):
            cause = u"用户名不合法，长度3到20,大小写字母、数字、-、下划线组成"
            print '2'
            return Response({
                'result':0,
                'cause':cause
                })

    avatar = request.FILES.get('avatar', None)
    if not avatar:
        print '3'
        return Response({
            'result': 0,
            'cause': u'必须上传头像'
            })

    ##### "注册到极光即时聊天" ######   
    JIM = 'https://api.im.jpush.cn/v1/users/'
    data = [{"username": username, "password": username},]
    data = json.dumps(data)
    base64_auth_string = base64.b64encode(app_key + ':' + master_secret)
    headers = dict()
    headers['Authorization'] = 'Basic ' + base64_auth_string
    headers["Content-type"] = "application/json;charset:utf-8"
    response = requests.post(JIM, data=data, headers=headers, verify=False)
    if  response.status_code != 201:
        print '4'
        return Response({
            "result": 0,
            "cause": u"注册失败",
            })
    ############
    new_user = User.objects.create_user(username=username, password=password)
    user_info = UserInfo.objects.create(user=new_user, nickname=new_user.id, gender=gender, avatar=avatar)
    token = Token.objects.create(user=new_user)

    serializer = UserInfoSerializer(user_info)
    response = serializer.data             
    response['token'] = token.key

    return Response({
        'result': 1,
        'user_info': response
        }, )


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
            }, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

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
    old_password = receive.get('old_password', None)
    new_password = receive.get('password', None)
    change_avatar = request.FILES.get('avatar', None)

    if change_avatar:
        UserInfo.objects.filter(user=user).update(avatar=change_avatar)
    
    if old_password and new_password:
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
        else:
            return Response({
                'result': 0,
                'cause': u'原密码错误'
                })

    if change_nickname:
        UserInfo.objects.filter(user=user).update(nickname=change_nickname)
    
    if change_gender and change_gender in ['0', '1']:
        UserInfo.objects.filter(user=user).update(gender=change_gender)
    
    return Response({
        'result': 1,
        })

# @api_view(['POST'])
# def upload_avatar(request):
#     user = request.user
#     avatar = request.FILES.get('avatar', None)
#     if not avatar:
#         return Response({
#             'result': 0,
#             'cause': u'没有上传图片'
#             })

#     if UserInfo(user=user).avatar_count < 9:
#     UploadAvatar.create(user=user, avatar=avatar)
        
