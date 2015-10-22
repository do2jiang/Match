# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_userinfo_nickname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='nickname',
            field=models.CharField(default='', max_length=20, blank=True),
            preserve_default=False,
        ),
    ]
