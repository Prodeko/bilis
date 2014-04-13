# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Game.winner_elo'
        db.add_column('bilis_game', 'winner_elo',
                      self.gf('django.db.models.fields.IntegerField')(default=1000),
                      keep_default=False)

        # Adding field 'Game.winner_fargo'
        db.add_column('bilis_game', 'winner_fargo',
                      self.gf('django.db.models.fields.IntegerField')(default=1000),
                      keep_default=False)

        # Adding field 'Game.loser_elo'
        db.add_column('bilis_game', 'loser_elo',
                      self.gf('django.db.models.fields.IntegerField')(default=1000),
                      keep_default=False)

        # Adding field 'Game.loser_fargo'
        db.add_column('bilis_game', 'loser_fargo',
                      self.gf('django.db.models.fields.IntegerField')(default=1000),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Game.winner_elo'
        db.delete_column('bilis_game', 'winner_elo')

        # Deleting field 'Game.winner_fargo'
        db.delete_column('bilis_game', 'winner_fargo')

        # Deleting field 'Game.loser_elo'
        db.delete_column('bilis_game', 'loser_elo')

        # Deleting field 'Game.loser_fargo'
        db.delete_column('bilis_game', 'loser_fargo')


    models = {
        'bilis.game': {
            'Meta': {'object_name': 'Game'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bilis.Player']", 'related_name': "'lost_games'"}),
            'loser_elo': ('django.db.models.fields.IntegerField', [], {}),
            'loser_fargo': ('django.db.models.fields.IntegerField', [], {}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'under_table': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'winner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bilis.Player']", 'related_name': "'won_games'"}),
            'winner_elo': ('django.db.models.fields.IntegerField', [], {}),
            'winner_fargo': ('django.db.models.fields.IntegerField', [], {})
        },
        'bilis.player': {
            'Meta': {'ordering': "['last_name', 'first_name']", 'object_name': 'Player'},
            'elo': ('django.db.models.fields.IntegerField', [], {}),
            'fargo': ('django.db.models.fields.IntegerField', [], {}),
            'favorite_color': ('django.db.models.fields.IntegerField', [], {'default': '16711680'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['bilis']