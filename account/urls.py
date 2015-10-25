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
    url(r'^settings', user.settings),
    url(r'^match_users/', friend.match_user_list),
    url(r'^check_user/', user.check_user),
    url(r'^link_user/', friend.link_user),
    url(r'^get_phone_friends/', friend.get_phone_friends),
)