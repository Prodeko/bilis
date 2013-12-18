from django.db import models

# Create your models here.

class Player(models.Model):
    name = models.CharField(max_length=100)
    score = models.FloatField()
    favorite_color = models.IntegerField()

class Game(models.Model):
    winner = models.ForeignKey(Player, related_name="won_games")
    loser = models.ForeignKey(Player, related_name="lost_games")
    under_table = models.BooleanField()


    
