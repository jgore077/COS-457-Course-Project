import csv
import json
import random
from faker import Faker # Installation: pip install Faker
from volleyBallDatabase import volleyBallDatabase
import psycopg2 # Installation: pip install psycopg2

from datetime import datetime

fake = Faker()

games_file = open('games.csv', 'w', newline='', encoding="utf-8")
write_game = csv.writer(games_file, delimiter=',', lineterminator='\n')
write_game.writerow(["game_id", "location", "description", "gamedate", "opponent", "match_score"])
# TABLE games("game_id", "location", "description", "gamedate", "opponent", "match_score", "set_scores")

game_id = 1 #starts at 1 and go up by 1 for each recorded/scheduled game
teams = ["University of New England", "University of Maine Orino", "University of New Hampshire", "Plymouth State University", "Merrimack College", "Colby College", "Bates College"]
# 100 different games
gamedate = [fake.date_time_between(start_date= "-2y", end_date= "+1y") for i in range(100)]
sorted_gamedates = sorted(gamedate) 
for date in sorted_gamedates:
    opponent = random.choice(teams)
    var = random.randint(1, 2)
    if var == 1:
        location = "USM"
    else:
        location = opponent
    description = "USM v.s. " + opponent + "! Located at " + location + " on " + str(date) + "."
#    if date < datetime.now(): #past, USM - Opponent
#        match_score = random.choice("3 - 0", "3 - 1", "3 - 2", "2 - 3", "1 - 3", "0 - 3")
#    else: #this is then a future game, so no score yet
#        match_score = None
    write_game.writerow([game_id, location, description, date, opponent, None])
    game_id += 1

games_file.close()
#games.csv file complete, now upload to SQL table
with open('config.json', 'r') as data:
    config = json.load(data)

connection = psycopg2.connect(**config)
cursor = connection.cursor()
vbDB = volleyBallDatabase(cursor= cursor, connection= connection)
#
csv_file_path = r'\Users\Megan Fleck\COS-457-Course-Project\games.csv'

with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    header = next(csv_reader)

    insert_query = f"INSERT INTO vbms.games VALUES ({', '.join(['%s'] * len(header))})"
    
    # Iterate through each row and execute the insert to the table
    for row in csv_reader:
        cursor.execute(insert_query, row)

connection.commit()

# Our games table is now filled with 100 different games of past and future.
# All match_score values are set as null for now. 
# For the games in the past we will generate a table for set scores.
# This then can be used to calculate the match score and update the games table.

#TABLE sets(game_id, set_num, usm_score, opponent_score)
sets_file = open('sets.csv', 'w', newline='', encoding="utf-8")
write_set = csv.writer(sets_file, delimiter=',', lineterminator='\n')
write_set.writerow(["game_id", "set_num", "usm_score", "opponent_score"])

# Method to produce random set score to 25, where team a wins with 25. e.g., [25, (any integer 1 - 23)]
def set_win():
    a_score = 25
    b_score = random.randint(1, 23)
    return [a_score, b_score]

cursor.execute("SELECT game_id, gamedate FROM vbms.games;")
gamesID = cursor.fetchall()

for gID in gamesID:
    if gID[1] < datetime.now(): #check if game is in past, if so then we need scores
        final_score = random.randint(1, 6) #match best of 5
        #here 1 - 6 represents the following possible match scores: "3 - 0", "3 - 1", "3 - 2", "2 - 3", "1 - 3", "0 - 3"
        if final_score == 1: # 3 - 0
            for i in range(1, 4):
                score = set_win()
                write_set.writerow([gID[0], i, score[0], score[1]]) #team1 win
        elif final_score == 2: # 3 - 1
            var = random.randint(1, 3)
            for i in range(1, 5):
                score = set_win()
                if i == var:
                    write_set.writerow([gID[0], i, score[1], score[0]]) #team2 win
                else:
                    write_set.writerow([gID[0], i, score[0], score[1]]) #team1 win
        elif final_score == 3: # 3 - 2
            var1 = random.randint(1, 4)
            var2 = random.randint(1, 4)
            while var1 == var2:
                var2 = random.randint(1, 4) #pick new var until these two are different
            for i in range(1, 6):
                score = set_win()
                if (i == var1) or (i == var2):
                    write_set.writerow([gID[0], i, score[1], score[0]]) #team2 win
                else:
                    write_set.writerow([gID[0], i, score[0], score[1]]) #team1 win
        elif final_score == 4: # 2 - 3
            var1 = random.randint(1, 4)
            var2 = random.randint(1, 4)
            while var1 == var2:
                var2 = random.randint(1, 4) #pick new var until these two are different
            for i in range(1, 6):
                score = set_win()
                if (i == var1) or (i == var2):
                    write_set.writerow([gID[0], i, score[0], score[1]]) #team1 win
                else:
                    write_set.writerow([gID[0], i, score[1], score[0]]) #team2 win
        elif final_score == 5: # 1 - 3
            var = random.randint(1, 3)
            for i in range(1, 5):
                if i == var:
                    write_set.writerow([gID[0], i, score[0], score[1]]) #team1 win
                else:
                    write_set.writerow([gID[0], i, score[1], score[0]]) #team2 win
        else: #final_score == 6: # 0 - 3
            for i in range(1, 4):
                score = set_win()
                write_set.writerow([gID[0], i, score[1], score[0]]) #team2 win

sets_file.close()
#sets.csv file is complete, now upload to SQL table

csv_file_path = r'\Users\Megan Fleck\COS-457-Course-Project\sets.csv'

with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    header = next(csv_reader)

    insert_query = f"INSERT INTO vbms.sets VALUES ({', '.join(['%s'] * len(header))})"
    
    # Iterate through each row and execute the insert to the table
    for row in csv_reader:
        cursor.execute(insert_query, row)

connection.commit()
cursor.close()
connection.close()

# Now update the games Table to include the match_scores, 
# may want to do this directly in PostgreSQL
#need to make sets table
