# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from couple.views import random

urlpatterns = patterns('',
    url(r'^random/list', random.random_list),
    url(r'^random/match/', random.random_match),
)
