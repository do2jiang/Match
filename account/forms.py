# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    username = forms.RegexField(regex=r'^[a-zA-Z0-9_]{3,15}')
    password = forms.CharField(min_length=6, max_length=64)
    password_confirm = forms.CharField()
    
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

    def clean_password_confirm(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password_confirm')
        if password1 != password2:
            raise forms.ValidationError(u'两次输入的密码不一致')

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
        