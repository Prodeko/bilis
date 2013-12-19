from django.db import models

# Create your models here.

class Player(models.Model):
    name = models.CharField(max_length=100)
    score = models.FloatField()
    favorite_color = models.IntegerField()
    def __unicode__(self):
    	return self.name

class Game(models.Model):
    winner = models.ForeignKey(Player, related_name="won_games")
    loser = models.ForeignKey(Player, related_name="lost_games")
    datetime = models.DateTimeField(auto_now=True)
    under_table = models.BooleanField()
    def __unicode__(self):
        return self.winner.name + " vs. " + self.loser.name + " " + self.datetime.strftime("%Y-%m-%d")

    
