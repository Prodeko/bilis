from datetime import datetime
from django.db import models
from django.db.models.signals import post_save
from bilis import utils

class Player(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    elo = models.DecimalField(decimal_places=2, max_digits=6)
    fargo = models.DecimalField(decimal_places=2, max_digits=6)
    favorite_color = models.IntegerField(default=16711680)
    def _get_name(self):
        return self.first_name + " " + self.last_name
    name = property(_get_name)
    def _get_favorite_color_string(self):
        return utils.int_to_html_color(self.favorite_color)
    favorite_color_string = property(_get_favorite_color_string)
    def _get_games(self):
        games = self.won_games.all() | self.lost_games.all()
        return sorted(games, key=lambda game: game.datetime, reverse=True)
    games = property(_get_games)
    def _get_games_count(self):
        return self.won_games.count() + self.lost_games.count()
    games_count = property(_get_games_count)
    def __str__(self):
        return "#{id} {name}".format(id=self.pk, name= self.name)
    def save(self, *args, **kwargs):
        if self.pk is None:
            self.elo = 100
            self.fargo = 100
        super(Player, self).save(*args, **kwargs)
    def update_rating(self, opponent_rating, result):
        if(result>0):
            change = round(10/(1+10**((self.elo - opponent_rating)/100)),1)
        else:
            change = round(-10/(1+10**((opponent_rating - self.elo)/100)),1)
        new_rating = self.elo + change
        self.elo = new_rating
        self.save()
        return change 

    def update_rating_fargo(self, opponent_rating, opponent_games, result):

        if (self.games>50): 
            self_robust = math.log(self.games,1.01029)-332.268
        else:
            self_robust = 50
        
        if (opponent_games>50): 
            opponent_robust = math.log(opponent_games,1.01029)-332.268
        else:
            opponent_robust = 50


        if (result>0):
            change = 630*(1-(1/(1+math.pow(2,((opponent_rating-self_rating)/100)))))*((opponent_robust-1)/(self_robust*opponent_robust))
        else:
            change = 630*(0-(1/(1+math.pow(2,((opponent_rating-self_rating)/100)))))*((opponent_robust-1)/(self_robust*opponent_robust))
        return change

    class Meta:
        ordering = ['last_name', 'first_name']

class Game(models.Model):
    winner = models.ForeignKey(Player, related_name="won_games")
    loser = models.ForeignKey(Player, related_name="lost_games")
    winner_elo = models.DecimalField(decimal_places=2, max_digits=6)
    winner_fargo = models.DecimalField(decimal_places=2, max_digits=6)
    loser_elo = models.DecimalField(decimal_places=2, max_digits=6)
    loser_fargo = models.DecimalField(decimal_places=2, max_digits=6)
    datetime = models.DateTimeField()
    under_table = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    def __str__(self):
        return self.winner.name + " vs. " + self.loser.name + " " + self.datetime.strftime("%Y-%m-%d")
    def save(self, *args, **kwargs):
        #TODO: implement rating calculation here
        winner_elo = self.winner.elo
        loser_elo = self.loser.elo
        self.winner.update_rating(loser_elo, 1)
        self.loser.update_rating(winner_elo, 0)
        if(self.datetime is None):
            self.datetime = datetime.now()
        self.winner_elo = self.winner.elo
        self.loser_elo = self.loser.elo
        self.winner_fargo = self.winner.fargo
        self.loser_fargo = self.loser.fargo
        super(Game, self).save(*args, **kwargs)
