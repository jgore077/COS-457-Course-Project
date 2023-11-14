import csv
import json
import random
from faker import Faker # Installation: pip install Faker
from volleyBallDatabase import volleyBallDatabase
import psycopg2 # Installation: pip install psycopg2

fake = Faker()

games_file = open('games.csv', 'w', newline='', encoding="utf-8")
write_game = csv.writer(games_file, delimiter=',', lineterminator='\n')
write_game.writerow(["game_id", "location", "description", "gamedate", "opponent", "match_score", "set_scores"])
# TABLE games("game_id", "location", "description", "gamedate", "opponent", "match_score", "set_scores")

teams = ["University of New England", "University of Maine Orino", "University of New Hampshire", "Plymouth State University", "Merrimack College", "Colby College", "Bates College"]
# 100 different games, if they on same day this will indicate tournament
gamedate = [fake.date_between(start_date= Date('2022-01-01'), end_date= ('2024-05-01')) for i in range(100)]
sorted_gamedates = sorted(gamedate) #issue with formatting of dates^
for date in sorted_gamedates:
    print(date)

opponent = random.choice(teams)
var = random.randint(1, 2)
if var == 1:
    location = "USM"
else:
    location = opponent

description = "USM v.s. " + opponent + "! Located at " + location + " on "