# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cela', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Etiqueta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('moderacio', models.CharField(default='E', max_length=1, choices=[('A', 'Aprobat'), ('R', 'Rebutjat'), ('E', 'En Tramit')])),
                ('nom', models.CharField(max_length=100)),
                ('slug', models.CharField(max_length=100, blank=True)),
                ('tipologia', models.CharField(default='E', max_length=1, choices=[('S', 'Sistema'), ('M', 'Moderacion'), ('Z', 'AreaContexto'), ('E', 'Etiqueta'), ('O', 'Objecte'), ('A', 'Adjectiu'), ('T', 'Temps'), ('L', 'Lloc'), ('P', 'Profesion')])),
                ('descripcio', models.TextField(verbose_name='descripció', blank=True)),
                ('wiki', models.URLField(default='', blank=True)),
                ('datahora', models.DateTimeField(auto_now_add=True)),
                ('cela', models.ForeignKey(to='cela.Cela', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tesauro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipo', models.CharField(max_length=1, choices=[('J', 'jerarquic'), ('S', 'sinonims'), ('A', 'antonims'), ('B', 'associatiu')])),
                ('etq1', models.ForeignKey(to='etiqueta.Etiqueta', related_name='element_fort')),
                ('etq2', models.ForeignKey(to='etiqueta.Etiqueta', related_name='element_debil')),
            ],
        ),
        migrations.AddField(
            model_name='etiqueta',
            name='relacio',
            field=models.ManyToManyField(to='etiqueta.Etiqueta', blank=True, through='etiqueta.Tesauro'),
        ),
    ]
