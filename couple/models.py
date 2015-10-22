# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

from account.fields import ThumbnailImageField

# Create your models here.
class RandomMath(models.Model):
	boy = models.ForeignKey(User, related_name='boy')
	girl = models.ForeignKey(User, related_name='girl')
	vote = models.IntegerField(default=1)
	
class LoveShow(models.Model):
	user = models.ForeignKey(User, related_name='love_show_user')
	lover = ThumbnailImageField(upload_to='media/love_show')
	favour = models.IntegerField(default=0)
	oppose = models.IntegerField(default=0)
	