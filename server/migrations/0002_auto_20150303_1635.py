# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='volunteer',
            name='sec_accept',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='volunteer',
            name='sec_edit',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
