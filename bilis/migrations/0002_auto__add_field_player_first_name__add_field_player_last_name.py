# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Player.first_name'
        db.add_column('bilis_player', 'first_name',
                      self.gf('django.db.models.fields.CharField')(max_length=50, default=''),
                      keep_default=False)

        # Adding field 'Player.last_name'
        db.add_column('bilis_player', 'last_name',
                      self.gf('django.db.models.fields.CharField')(max_length=50, default=''),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Player.first_name'
        db.delete_column('bilis_player', 'first_name')

        # Deleting field 'Player.last_name'
        db.delete_column('bilis_player', 'last_name')


    models = {
        'bilis.game': {
            'Meta': {'object_name': 'Game'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bilis.Player']", 'related_name': "'lost_games'"}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'under_table': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'winner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bilis.Player']", 'related_name': "'won_games'"})
        },
        'bilis.player': {
            'Meta': {'object_name': 'Player'},
            'favorite_color': ('django.db.models.fields.IntegerField', [], {'default': '16711680'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'live_rating': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'rating': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['bilis']