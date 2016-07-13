# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mailhelper', '0002_maillog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maillog',
            name='body_field',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='maillog',
            name='from_field',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='maillog',
            name='to_field',
            field=models.EmailField(max_length=254),
        ),
    ]
