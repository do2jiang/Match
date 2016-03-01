#encoding=utf-8
from celery import shared_task
from couple.models import LoveShow

from __future__ import absolute_import

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celeryapp import app as celery_app

#Rewritten code from /r2/r2/lib/db/_sorts.pyx
 
from datetime import datetime, timedelta
from math import log
 
epoch = datetime(1970, 1, 1)
 
def epoch_seconds(date):
    """Returns the number of seconds from the epoch to date."""
    td = date - epoch
    return td.days * 86400 + td.seconds + (float(td.microseconds) / 1000000)
 
def score(ups, downs):
    return ups - downs
 
def hot(ups, downs, date):
    """The hot formula. Should match the equivalent function in postgres."""
    s = score(ups, downs)
    order = log(max(abs(s), 1), 10)
    sign = 1 if s > 0 else -1 if s < 0 else 0
    seconds = epoch_seconds(date) - 1134028003
    return round(order + sign * seconds / 45000, 7)

# @shared_task
def update_love_show_hot():
    love_shows = LoveShow.objects.all()
    date = datetime(2015, 10, 25)
    for love_show in love_shows:
        love_show.hot = hot(love_show.favour, love_show.oppose, date)
        love_show.save()
        
        