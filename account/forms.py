# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User

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
        