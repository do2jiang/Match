# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from account.views import user, friend


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'xp.views.home', name='home'),
    # url(r'^xp/', include('xp.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^register', user.register),
    url(r'^login', user.login),
    url(r'^match_users/', friend.match_user_list),
    url(r'^get_user_avatar/', user.get_user_avatar),
)