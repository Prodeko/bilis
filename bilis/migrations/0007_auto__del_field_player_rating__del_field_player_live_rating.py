# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Player.rating'
        db.delete_column('bilis_player', 'rating')

        # Deleting field 'Player.live_rating'
        db.delete_column('bilis_player', 'live_rating')


    def backwards(self, orm):
        # Adding field 'Player.rating'
        db.add_column('bilis_player', 'rating',
                      self.gf('django.db.models.fields.IntegerField')(default=1000),
                      keep_default=False)

        # Adding field 'Player.live_rating'
        db.add_column('bilis_player', 'live_rating',
                      self.gf('django.db.models.fields.IntegerField')(default=1000),
                      keep_default=False)


    models = {
        'bilis.game': {
            'Meta': {'object_name': 'Game'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loser': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'lost_games'", 'to': "orm['bilis.Player']"}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'under_table': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'winner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'won_games'", 'to': "orm['bilis.Player']"})
        },
        'bilis.player': {
            'Meta': {'object_name': 'Player', 'ordering': "['last_name', 'first_name']"},
            'elo': ('django.db.models.fields.IntegerField', [], {}),
            'fargo': ('django.db.models.fields.IntegerField', [], {}),
            'favorite_color': ('django.db.models.fields.IntegerField', [], {'default': '16711680'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['bilis']