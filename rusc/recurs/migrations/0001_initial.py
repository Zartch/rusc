# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import rusc.recurs.models


class Migration(migrations.Migration):

    dependencies = [
        ('cela', '0001_initial'),
        ('etiqueta', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recurs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('moderacio', models.CharField(choices=[('A', 'Aprobat'), ('R', 'Rebutjat'), ('E', 'En Tramit')], max_length=1, default='E')),
                ('url', models.TextField()),
                ('descripcio', models.TextField(default='', blank=True)),
                ('datahora', models.DateTimeField(auto_now_add=True)),
                ('autor', models.CharField(default='', max_length=100, blank=True)),
                ('adjunt', models.FileField(upload_to='documents/%Y/%m/%d', null=True, validators=[rusc.recurs.models.Recurs.validate_file])),
                ('cela', models.ForeignKey(blank=True, to='cela.Cela')),
                ('etiquetes', models.ManyToManyField(blank=True, to='etiqueta.Etiqueta')),
                ('post_debat', models.ForeignKey(to='post.Post', verbose_name='recurs', null=True)),
            ],
        ),
    ]
