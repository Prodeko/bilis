# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        for player in orm.Player.objects.all():
            player.elo = player.live_rating
            player.fargo = player.rating
            player.save()

    def backwards(self, orm):
        for player in orm.Player.objects.all():
            player.live_rating = player.elo
            player.rating = player.fargo
            player.save()
    models = {
        'bilis.game': {
            'Meta': {'object_name': 'Game'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bilis.Player']", 'related_name': "'lost_games'"}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'under_table': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'winner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bilis.Player']", 'related_name': "'won_games'"})
        },
        'bilis.player': {
            'Meta': {'ordering': "['last_name', 'first_name']", 'object_name': 'Player'},
            'elo': ('django.db.models.fields.IntegerField', [], {}),
            'fargo': ('django.db.models.fields.IntegerField', [], {}),
            'favorite_color': ('django.db.models.fields.IntegerField', [], {'default': '16711680'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'live_rating': ('django.db.models.fields.IntegerField', [], {}),
            'rating': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['bilis']
    symmetrical = True
