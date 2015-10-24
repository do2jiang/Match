# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('couple', '0002_loveshow'),
    ]

    operations = [
        migrations.AddField(
            model_name='loveshow',
            name='hot',
            field=models.FloatField(default=0.0),
            preserve_default=True,
        ),
    ]
