from django.conf.urls import patterns, include, url
from django.contrib import admin
import os
DIRNAME = os.path.dirname(os.path.dirname(__file__))

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'match.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/', include('account.urls')),
    url(r'^couple/', include('couple.urls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(DIRNAME, "media"), 'show_indexes': True }),
)
