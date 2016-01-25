# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import rusc.usuari.models


class Migration(migrations.Migration):

    dependencies = [
        ('etiqueta', '__first__'),
        ('post', '__first__'),
        ('cela', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('visible', models.BooleanField(default=False)),
                ('etq', models.ForeignKey(to='etiqueta.Etiqueta')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('website', models.URLField(null=True)),
                ('avatar', models.FileField(null=True, validators=[rusc.usuari.models.UserProfile.validate_image], upload_to='profiles/%Y/%m/%d')),
                ('tipusSubscripcio', models.CharField(max_length=1, default='S', choices=[('T', 'Total'), ('S', 'Nomes subscrits. Subscriure automaticament'), ('X', 'Nomes subscrits: No subscriure automaticament')])),
                ('estat', models.CharField(max_length=1, default='A', choices=[('A', 'Acceptat'), ('E', 'En Tramit'), ('R', 'Rebutjat'), ('T', 'Troll')])),
                ('mailConf', models.CharField(max_length=1, default='E', choices=[('N', 'No Enviar Mails'), ('E', 'Enviar Tots el Mails')])),
                ('email_p', models.EmailField(max_length=254, blank=True)),
                ('dato_veri', models.CharField(max_length=150, blank=True)),
                ('cela', models.ForeignKey(to='cela.Cela')),
                ('etiquetes', models.ManyToManyField(to='etiqueta.Etiqueta', through='usuari.UserInfo', blank=True)),
                ('subscripcions', models.ManyToManyField(related_name='subscripcions', to='post.Post', blank=True)),
                ('user', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='userinfo',
            name='usr',
            field=models.ForeignKey(to='usuari.UserProfile'),
        ),
        migrations.AlterUniqueTogether(
            name='userprofile',
            unique_together=set([('cela', 'user')]),
        ),
    ]
