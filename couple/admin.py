# -*- coding: utf-8 -*-
from django.contrib import admin
from couple.models import RandomMath, LoveShow

class LoveShowAdmin(admin.ModelAdmin):
	list_display =  ('user', 'lover', 'favour', 'oppose')

class RandomMathAdmin(admin.ModelAdmin):
	list_display = ('boy', 'girl', 'vote')

admin.site.register(RandomMath, RandomMathAdmin)
admin.site.register(LoveShow, LoveShowAdmin)
