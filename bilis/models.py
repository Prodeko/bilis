from django.core.urlresolvers import reverse
from datetime import datetime, timedelta
from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from bilis import utils
import math

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
    
    '''
    ei ehka kovin hyva tapa toteuttaa, koska joutuu kaymaan for-loopilla kaikki pelaajat lapi
    
    def get_ranking(self):
        players = Player.objects.order_by('-fargo')
        ranking = 0
        for p in players:
            ranking += 1
            if p.pk == self.pk:
                break
        return ranking
    '''
    
    def get_victory_percent(self):
        if self._get_games_count() > 0:
            return '{:.2%}'.format(self.won_games.count() / self._get_games_count())
        else:
            return '{:.2%}'.format(0.0)
    
    def get_max_rating(self):
        if self.won_games.exists():
            won_games_max = self.won_games.all().aggregate(models.Max('winner_fargo'))['winner_fargo__max']
        else:
            won_games_max = 400
        if self.lost_games.exists():
            lost_games_max = self.lost_games.all().aggregate(models.Max('loser_fargo'))['loser_fargo__max']
        else:
            lost_games_max = 400
        if won_games_max > lost_games_max:
            max_rating = won_games_max
        else:
            max_rating = lost_games_max
        return max(max_rating, 400)
    
    def get_min_rating(self):
        if self.won_games.exists():
            won_games_min = self.won_games.all().aggregate(models.Min('winner_fargo'))['winner_fargo__min']
        else:
            won_games_min = 400
        if self.lost_games.exists():
            lost_games_min = self.lost_games.all().aggregate(models.Min('loser_fargo'))['loser_fargo__min']
        else:
            lost_games_min = 400
        if won_games_min < lost_games_min:
            min_rating = won_games_min
        else:
            min_rating = lost_games_min
        return min(min_rating, 400)
    
    def get_first_game_datetime(self):
        if self.won_games.exists():
            won_games_first_datetime = self.won_games.all().aggregate(models.Min('datetime'))['datetime__min']
        else:
            won_games_first_datetime = timezone.now()
        if self.lost_games.exists():
            lost_games_first_datetime = self.lost_games.all().aggregate(models.Min('datetime'))['datetime__min']
        else:
            lost_games_first_datetime = timezone.now()
        if won_games_first_datetime < lost_games_first_datetime:
            first_datetime = won_games_first_datetime
        else:
            first_datetime = lost_games_first_datetime
        return first_datetime
    
    def get_last_game_datetime(self):
        if self.won_games.exists():
            won_games_last_datetime = self.won_games.all().aggregate(models.Max('datetime'))['datetime__max']
        else:
            won_games_last_datetime = timezone.now()
        if self.lost_games.exists():
            lost_games_last_datetime = self.lost_games.all().aggregate(models.Max('datetime'))['datetime__max']
        else:
            lost_games_last_datetime = timezone.now()
        if won_games_last_datetime < lost_games_last_datetime:
            last_datetime = won_games_last_datetime
        else:
            last_datetime = lost_games_last_datetime
        return last_datetime
    
    def get_games_per_day(self):
        days_between_first_and_last = self.get_last_game_datetime().date() - self.get_first_game_datetime().date() + timedelta(1)
        return '{:.2}'.format(self._get_games_count() / days_between_first_and_last.days)

    def get_last_game_date_str(self):
        if len(self._get_games()) > 0:
            last_datetime = self.get_last_game_datetime()
            if last_datetime.date() == timezone.now().date():
                last_time = last_datetime.time()
            else:
                last_time = last_datetime.date()
        else:
            last_time = '-'
        return str(last_time)
    
    def is_active(self):
        # ei-aktiivinen jos alle 30 pelia ja yli 100 pv tauko pelaamisesta.
        if timezone.now().date() - self.get_last_game_datetime().date() > timedelta(100):
            if self._get_games_count() < 30:
                return False
        else:
            return True
    
    def __str__(self):
        return "#{id} {name} ({rating})".format(id=self.pk, name= self.name, rating=self.fargo)
    def get_rating(self, type):
        if type == "elo":
            return self.elo
        else:
            return self.fargo
    def save(self, *args, **kwargs):
        if self.pk is None:
            self.elo = 100
            self.fargo = 400
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

        if (len(self.games) > 20): 
            self_robust = math.log(len(self.games), 1.14163) - 2.61648
        else:
            self_robust = 20
        
        if (opponent_games > 20): 
            opponent_robust = math.log(opponent_games, 1.14163) - 2.61648
        else:
            opponent_robust = 20


        if (result>0):
            change = 630*(1-(1/(1+math.pow(2,((opponent_rating-self.fargo)/100)))))*((opponent_robust-1)/(self_robust*opponent_robust))
        else:
            change = 630*(0-(1/(1+math.pow(2,((opponent_rating-self.fargo)/100)))))*((opponent_robust-1)/(self_robust*opponent_robust))
        self.fargo = float(self.fargo) + float(change)
        self.save()
        cache.delete('fargo_series_' + str(self.pk))
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
    deleted = models.BooleanField(default=False)
    def get_winner_rating(self, type):
        return self.winner_elo if type == "elo" else self.winner_fargo
    def get_loser_rating(self, type):
        return self.loser_elo if type == "elo" else self.loser_fargo
    def __str__(self):
        return self.winner.name + " vs. " + self.loser.name + " " + self.datetime.strftime("%Y-%m-%d")
    def save(self, *args, **kwargs):
        if self.pk is None:
            if Game.objects.count() > 0:
                game = Game.objects.latest('datetime')
                if(game.deleted):
                    game.delete()
            winner_elo = self.winner.elo
            loser_elo = self.loser.elo
            winner_fargo = self.winner.fargo
            loser_fargo = self.loser.fargo
            self.winner_elo = self.winner.elo
            self.loser_elo = self.loser.elo
            self.winner_fargo = self.winner.fargo
            self.loser_fargo = self.loser.fargo
            self.winner.update_rating(loser_elo, 1)
            self.loser.update_rating(winner_elo, 0)
            self.winner.update_rating_fargo(loser_fargo, self.loser.games_count, 1)
            self.loser.update_rating_fargo(winner_fargo, self.winner.games_count, 0)
            if(self.datetime is None):
                self.datetime = datetime.now()
        
        super(Game, self).save(*args, **kwargs)
        
    def replay(self, *args, **kwargs):
        winner_elo = self.winner.elo
        loser_elo = self.loser.elo
        winner_fargo = self.winner.fargo
        loser_fargo = self.loser.fargo
        self.winner_elo = self.winner.elo
        self.loser_elo = self.loser.elo
        self.winner_fargo = self.winner.fargo
        self.loser_fargo = self.loser.fargo
        self.winner.update_rating(loser_elo, 1)
        self.loser.update_rating(winner_elo, 0)
        self.winner.update_rating_fargo(loser_fargo, self.loser.games_count, 1)
        self.loser.update_rating_fargo(winner_fargo, self.winner.games_count, 0)
        self.save()
        
def update_all_ratings():
    for player in Player.objects.all():
        player.elo = 100
        player.fargo = 400
        player.save()
        
    for game in Game.objects.all():
        game.replay()
