# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Player.elo'
        db.alter_column('bilis_player', 'elo', self.gf('django.db.models.fields.DecimalField')(decimal_places=2, max_digits=6))

        # Changing field 'Player.fargo'
        db.alter_column('bilis_player', 'fargo', self.gf('django.db.models.fields.DecimalField')(decimal_places=2, max_digits=6))

        # Changing field 'Game.winner_fargo'
        db.alter_column('bilis_game', 'winner_fargo', self.gf('django.db.models.fields.DecimalField')(decimal_places=2, max_digits=6))

        # Changing field 'Game.loser_elo'
        db.alter_column('bilis_game', 'loser_elo', self.gf('django.db.models.fields.DecimalField')(decimal_places=2, max_digits=6))

        # Changing field 'Game.loser_fargo'
        db.alter_column('bilis_game', 'loser_fargo', self.gf('django.db.models.fields.DecimalField')(decimal_places=2, max_digits=6))

        # Changing field 'Game.winner_elo'
        db.alter_column('bilis_game', 'winner_elo', self.gf('django.db.models.fields.DecimalField')(decimal_places=2, max_digits=6))

    def backwards(self, orm):

        # Changing field 'Player.elo'
        db.alter_column('bilis_player', 'elo', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'Player.fargo'
        db.alter_column('bilis_player', 'fargo', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'Game.winner_fargo'
        db.alter_column('bilis_game', 'winner_fargo', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'Game.loser_elo'
        db.alter_column('bilis_game', 'loser_elo', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'Game.loser_fargo'
        db.alter_column('bilis_game', 'loser_fargo', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'Game.winner_elo'
        db.alter_column('bilis_game', 'winner_elo', self.gf('django.db.models.fields.IntegerField')())

    models = {
        'bilis.game': {
            'Meta': {'object_name': 'Game'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bilis.Player']", 'related_name': "'lost_games'"}),
            'loser_elo': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'max_digits': '6'}),
            'loser_fargo': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'max_digits': '6'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'under_table': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'winner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bilis.Player']", 'related_name': "'won_games'"}),
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