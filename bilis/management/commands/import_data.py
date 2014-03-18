from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.utils import timezone
from django.conf import settings
from csv import * 
from bilis.models import *
import math
from time import strptime, mktime
from datetime import datetime
import warnings
warnings.filterwarnings(
                'error', r"DateTimeField .* received a naive datetime",
                        RuntimeWarning, r'django\.db\.models\.fields')

class Command(BaseCommand):
    help = """read in data from a csv file\n
    default files (use these, none else supported for now..):\n
    \tbilis_players.csv (format: id;name;live_rating)\n
    \tbilis_games.csv (format: date;time;winner;(winner_rating);loser;(loser_rating))\n
    \tdate %m/%d/%Y %I:%M:%S %p"""

    def import_players(self, filename='bilis_players.csv'):
        file = open(filename, encoding='utf-8')
        reader = DictReader(file, delimiter=';')
        for row in reader:
            first_name = row['name'].split(' ')[0]
            last_name = " ".join(row['name'].split(' ')[1:])
            id = row['id']
            live_rating = int(math.floor(float(row['live_rating'])))
            #print (first_name + " " + last_name)
            #print (live_rating)
            print (id)
            p = Player.objects.create(pk=id, first_name=first_name, last_name=last_name, live_rating=live_rating, rating=live_rating)
            p.save()

    def import_games(self, filename='bilis_games.csv'):
        file = open(filename, encoding='utf-8')
        reader = DictReader(file, delimiter=';')
        for row in reader:
            if not row['winner'] or not row['loser']:
                continue
            datetimestr = row['date'] + " " + row['time'] 
            try:
                dt = timezone.make_aware(datetime.fromtimestamp(mktime((strptime(datetimestr, "%m/%d/%Y %I:%M:%S %p")))), timezone.get_default_timezone())
            except(ValueError):
                print("FAIL: " + datetimestr)
            winner = Player.objects.get(pk=row['winner'])
            loser = Player.objects.get(pk=row['loser'])
            g = Game.objects.create(datetime=dt, winner=winner, loser=loser)
            g.save()
            print(g.pk)

    def handle(self, *args, **options):
        self.import_players() 
        self.import_games()
