# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('winner_elo', models.DecimalField(decimal_places=2, max_digits=6)),
                ('winner_fargo', models.DecimalField(decimal_places=2, max_digits=6)),
                ('loser_elo', models.DecimalField(decimal_places=2, max_digits=6)),
                ('loser_fargo', models.DecimalField(decimal_places=2, max_digits=6)),
                ('datetime', models.DateTimeField()),
                ('under_table', models.BooleanField(default=False)),
                ('notes', models.TextField(blank=True)),
                ('deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('elo', models.DecimalField(decimal_places=2, max_digits=6)),
                ('fargo', models.DecimalField(decimal_places=2, max_digits=6)),
                ('favorite_color', models.IntegerField(default=16711680)),
            ],
            options={
                'ordering': ['last_name', 'first_name'],
            },
        ),
        migrations.AddField(
            model_name='game',
            name='loser',
            field=models.ForeignKey(related_name='lost_games', to='bilis.Player'),
        ),
        migrations.AddField(
            model_name='game',
            name='winner',
            field=models.ForeignKey(related_name='won_games', to='bilis.Player'),
        ),
    ]
