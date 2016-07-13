# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mailhelper', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MailLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('from_field', models.CharField(max_length=200)),
                ('to_field', models.CharField(max_length=200)),
                ('subject_field', models.CharField(max_length=200)),
                ('body_field', models.CharField(max_length=1024)),
                ('send_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
