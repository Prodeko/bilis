# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Player'
        db.create_table('bilis_player', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('rating', self.gf('django.db.models.fields.IntegerField')()),
            ('live_rating', self.gf('django.db.models.fields.IntegerField')()),
            ('favorite_color', self.gf('django.db.models.fields.IntegerField')(default=16711680)),
        ))
        db.send_create_signal('bilis', ['Player'])

        # Adding model 'Game'
        db.create_table('bilis_game', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('winner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='won_games', to=orm['bilis.Player'])),
            ('loser', self.gf('django.db.models.fields.related.ForeignKey')(related_name='lost_games', to=orm['bilis.Player'])),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('under_table', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('bilis', ['Game'])


    def backwards(self, orm):
        # Deleting model 'Player'
        db.delete_table('bilis_player')

        # Deleting model 'Game'
        db.delete_table('bilis_game')


    models = {
        'bilis.game': {
            'Meta': {'object_name': 'Game'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loser': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'lost_games'", 'to': "orm['bilis.Player']"}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'under_table': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'winner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'won_games'", 'to': "orm['bilis.Player']"})
        },
        'bilis.player': {
            'Meta': {'object_name': 'Player'},
            'favorite_color': ('django.db.models.fields.IntegerField', [], {'default': '16711680'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'live_rating': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'rating': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['bilis']