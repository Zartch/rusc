# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuari', '0002_auto_20160121_0146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='mailConf',
            field=models.CharField(max_length=1, default='E', choices=[('N', 'No Enviar Mails'), ('E', 'Enviar Tots el Mails')]),
        ),
    ]
