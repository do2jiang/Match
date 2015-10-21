from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class RandomMath(models.Model):
	boy = models.ForeignKey(User, related_name='boy')
	girl = models.ForeignKey(User, related_name='girl')
	vote = models.IntegerField(default=1)
	
