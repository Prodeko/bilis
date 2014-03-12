from __future__ import division
from django.db import models
from django.db.models.signals import post_save
# Create your models here.

class Player(models.Model):
    name = models.CharField(max_length=100)
    rating = models.IntegerField()
    live_rating = models.IntegerField()
    favorite_color = models.IntegerField(default=16711680)
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if self.pk is None:
            self.rating = 1000
            self.live_rating = 1000
        super(Player, self).save(*args, **kwargs)
    def update_rating(self, opponent_rating, result):
        change = result * (self.live_rating / opponent_rating) * 10
        self.live_rating = self.live_rating + change
        self.save()
        return change 

class Game(models.Model):
    winner = models.ForeignKey(Player, related_name="won_games")
    loser = models.ForeignKey(Player, related_name="lost_games")
    datetime = models.DateTimeField(auto_now=True)
    under_table = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    def __str__(self):
        return self.winner.name + " vs. " + self.loser.name + " " + self.datetime.strftime("%Y-%m-%d")
    def save(self, *args, **kwargs):
        self.winner.update_rating(self.loser.live_rating, 1)
        self.loser.update_rating(self.winner.live_rating, -1)
        super(Game, self).save(*args, **kwargs)
