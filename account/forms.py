# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User

error_messages = {
    'username': {
        'required': u'必须填写用户名',
        'min_length': u'用户名长度过短（3-12个字符）',
        'max_length': u'用户名长度过长（3-12个字符）',
        'invalid': u'用户名格式错误（英文字母开头，数字，下划线构成）'
    },
    'email': {
        'required': u'必须填写E-mail',
        'min_length': u'Email长度有误',
        'max_length': u'Email长度有误',
        'invalid': u'Email地址无效'
    },
    'password': {
        'required': u'必须填写密码',
        'min_length': u'密码长度过短（6-64个字符）',
        'max_length': u'密码长度过长（6-64个字符）'
    },
}

class RegisterForm(forms.ModelForm):
    username = forms.RegexField(regex=r'^[a-zA-Z0-9_]{3,15}')
    password = forms.CharField(min_length=6, max_length=64)

    class Meta:
        model = User
        fields = ('username',)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
            raise forms.ValidationError(u'用户名已被注册')
        except User.DoesNotExist:
            return username

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class SettingPasswordForm(forms.Form):
    password_old = forms.CharField(min_length=6, max_length=64,
        error_messages=error_messages.get('password'))
    password = forms.CharField(min_length=6, max_length=64,
        error_messages=error_messages.get('password'))

    def __init__(self, request):
        self.user = request.user
        super(SettingPasswordForm, self).__init__(request.POST)

    def clean(self):
        password_old = self.cleaned_data.get('password_old')
        password = self.cleaned_data.get('password')

        if not (password_old and self.user.check_password(password_old)):
            raise forms.ValidationError(u'当前输入旧密码有误')
            
        return self.cleaned_data

