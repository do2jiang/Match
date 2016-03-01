from __future__ import absolute_import

from celery import shared_task
import time
from  match import settings
import jpush
from campus.models import Concern

@shared_task
def jpush_message(username, link_username):
    _jpush = jpush.JPush(settings.app_key, settings.master_secret)
    push = _jpush.create_push()

    push.audience = jpush.audience(
        {'alias':[username]},
    )

    extras = {
        'username': user.username,
        'title': topic.title,
        'created': timestamp,
        'describe': topic.describe,
        'content_url': topic.content_url,
        'first_image': topic.first_image,
    }
    
    push.message = jpush.message(msg_content='0', extras=extras)
    push.platform = jpush.all_
    push.send()