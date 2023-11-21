
import csv
import json
import random
from faker import Faker # Installation: pip install Faker
from volleyBallDatabase import volleyBallDatabase
import psycopg2 # Installation: pip install psycopg2

fake = Faker()

practice_file = open('practice.csv', 'w', newline='', encoding="utf-8")
write_practice = csv.writer(practice_file, delimiter=',', lineterminator='\n')
write_practice.writerow(["description", "location", "date"])

desc1 = ["Mandatory Practice", "Open Gym", "Combined practice with mens team", "Optional Practice", "Setting Clinic", "Hitting Clinic", "Passing Clinic", "Rotations overview"]
desc2 = [" ", "Remember to bring knee pads!", "Remember to let us know if you can not make it!", "So excited to see you all there!", "Drive Safe!"]
gym = ["Gorham Gym", "Portland Gym"]

dates = [fake.date_time_between(start_date= "-2y", end_date= "+1y") for i in range(200)]
sorted_dates = sorted(dates)
# create 200 practices for the past 2 years
for date in sorted_dates:
    location = random.choice(gym)
    description = random.choice(desc1) + ". " + random.choice(desc2)
    write_practice.writerow([description, location, date])

practice_file.close()
# csv file complete, now upload to table

with open('config.json', 'r') as data:
    config = json.load(data)

connection = psycopg2.connect(**config)
cursor = connection.cursor()
vbDB = volleyBallDatabase(cursor= cursor, connection= connection)

csv_file_path = './practice.csv'

with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    header = next(csv_reader)
    
    # Iterate through each row and insert using  the function defined in volleyBallDatabase.py
    for row in csv_reader:
        vbDB.insert_practice(row[0], row[1], row[2])

cursor.close()
connection.close()
    
