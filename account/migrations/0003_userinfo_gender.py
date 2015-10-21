# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='gender',
            field=models.CharField(blank=True, max_length=1, null=True, choices=[('1', 'female'), ('0', 'man')]),
            preserve_default=True,
        ),
    ]
