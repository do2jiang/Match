# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

from account.fields import ThumbnailImageField

class UserInfo(models.Model):
    user = models.OneToOneField(User, related_name='userinfo')
    nickname = models.CharField(max_length=20, blank=True,)
    avatar = ThumbnailImageField(upload_to='account/avatar')
    GENDER = ( (u'1', u'female'), (u'0', u'man'), )
    gender = models.CharField(max_length = 1, choices = GENDER, blank = True, null = True)

    def __unicode__(self):
        return self.user.username

import binascii
import os

class Token(models.Model):
    key = models.CharField(max_length=40, unique=True, primary_key=True)
    user = models.OneToOneField(User,  related_name='token')
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(Token, self).save(*args, **kwargs)

    def update(self):
        self.key = self.generate_key()
        super(Token, self).save()
        return self.key

    def generate_key(self):
        return binascii.hexlify(os.urandom(3)).decode() 

    def __unicode__(self):
        return self.key + ' ' + self.user.username