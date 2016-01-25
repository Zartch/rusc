# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('cela', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Pregunta',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('text', models.TextField()),
                ('answer', models.TextField(blank=True)),
                ('sort_order', models.IntegerField(default=0)),
                ('created_on', models.DateTimeField(default=datetime.datetime.now)),
                ('updated_on', models.DateTimeField(default=datetime.datetime.now)),
                ('cela', models.ForeignKey(related_name='cela_FAQ', to='cela.Cela')),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, related_name='pregunta_created')),
                ('updated_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, related_name='pregunta_updated')),
            ],
        ),
    ]
