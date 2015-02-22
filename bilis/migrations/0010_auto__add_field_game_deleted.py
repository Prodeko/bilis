# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Game.deleted'
        db.add_column('bilis_game', 'deleted',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Game.deleted'
        db.delete_column('bilis_game', 'deleted')


    models = {
        'bilis.game': {
            'Meta': {'object_name': 'Game'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loser': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'lost_games'", 'to': "orm['bilis.Player']"}),
            'loser_elo': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'max_digits': '6'}),
            'loser_fargo': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'max_digits': '6'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'under_table': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'winner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'won_games'", 'to': "orm['bilis.Player']"}),
            'winner_elo': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'max_digits': '6'}),
            'winner_fargo': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'max_digits': '6'})
        },
        'bilis.player': {
            'Meta': {'object_name': 'Player', 'ordering': "['last_name', 'first_name']"},
            'elo': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'max_digits': '6'}),
            'fargo': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'max_digits': '6'}),
            'favorite_color': ('django.db.models.fields.IntegerField', [], {'default': '16711680'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['bilis']