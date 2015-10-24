# #encoding=utf-8
# from celery import shared_task
# from couple.models import LoveShow

# from __future__ import absolute_import

# # This will make sure the app is always imported when
# # Django starts so that shared_task will use this app.
# from .celeryapp import app as celery_app

# @shared_task
# def update_love_show_hot():
#     love_shows = LoveShow.objects.all()
#     for love_show in love_shows:
#         love_show.hot = 
#         