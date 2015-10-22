# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import account.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('couple', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoveShow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lover', account.fields.ThumbnailImageField(upload_to=b'media/love_show')),
                ('favour', models.IntegerField(default=0)),
                ('oppose', models.IntegerField(default=0)),
                ('user', models.ForeignKey(related_name='love_show_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
