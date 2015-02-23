from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.utils import timezone
from django.conf import settings
from csv import * 
from bilis.models import *
import math
from time import strptime, mktime
from random import randint
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
            elo = 100
            fargo = 400
            print (id)
            p = Player.objects.create(pk=id, first_name=first_name, last_name=last_name, elo=elo, fargo=fargo, favorite_color=randint(0,16711680))
            p.save()

    def import_games(self, filename='bilis_games.csv'):
        file = open(filename, encoding='utf-8')
        reader = DictReader(file, delimiter=';')
        num_lines = sum(1 for line in open(filename, encoding='utf-8'))-1

        rows_in = 0 
        rows_out = 0
        rows_rejected = 0
        for row in reader:
            rows_in = rows_in + 1
            if not row['winner'] or not row['loser']:
                print("empty row")
                rows_rejected = rows_rejected+1
                continue
            datetimestr = row['date'] + " " + row['time'] 
            try:
                dt = timezone.make_aware(datetime.fromtimestamp(mktime((strptime(datetimestr, "%m/%d/%Y %I:%M:%S %p")))), timezone.get_default_timezone())
            except(ValueError):
                print("FAIL: " + datetimestr)
                rows_rejected = rows_rejected+1
                continue
            winner = Player.objects.get(pk=row['winner'])
            loser = Player.objects.get(pk=row['loser'])
            try:
                g = Game.objects.create(datetime=dt, winner=winner, loser=loser)
                g.save()
            except:
                print("{} {} {}".format(dt, winner, loser))
                rows_rejected = rows_rejected+1
                continue
            rows_out = rows_out + 1
        print("Read in {rows_in} of {total}".format(rows_in=rows_in, total=num_lines))
        print("Successfully processed {rows_out}, rejected {rows_rejected}".format(rows_out=rows_out, rows_rejected=rows_rejected))

    def handle(self, *args, **options):
        self.import_players() 
        self.import_games()
