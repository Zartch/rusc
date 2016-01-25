# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recurs', '__first__'),
        ('etiqueta', '__first__'),
        ('cela', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('moderacio', models.CharField(default='E', choices=[('A', 'Aprobat'), ('R', 'Rebutjat'), ('E', 'En Tramit')], max_length=1)),
                ('titol', models.CharField(max_length=40)),
                ('text', models.TextField()),
                ('datahora', models.DateTimeField(auto_now_add=True)),
                ('rank_score', models.FloatField(default=0.0)),
                ('num_comments', models.IntegerField(default=0)),
                ('autor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('cela', models.ForeignKey(blank=True, related_name='posts', to='cela.Cela')),
                ('etiquetes', models.ManyToManyField(blank=True, to='etiqueta.Etiqueta')),
                ('pare', models.ForeignKey(blank=True, null=True, related_name='children', to='post.Post')),
                ('recursos', models.ManyToManyField(blank=True, to='recurs.Recurs')),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('post', models.ForeignKey(to='post.Post')),
                ('voter', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
