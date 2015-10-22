# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from couple.views import random, love_show

urlpatterns = patterns('',
    url(r'^random/list', random.random_list),
    url(r'^random/match/', random.random_match),
    url(r'^love_show/get', love_show.lovers_get),
)
