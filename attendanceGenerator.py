import json
import random
from faker import Faker # Installation: pip install Faker
from volleyBallDatabase import volleyBallDatabase
import psycopg2 # Installation: pip install psycopg2
from datetime import datetime

with open('config.json', 'r') as data:
    config = json.load(data)

connection = psycopg2.connect(**config)
cursor = connection.cursor()
vbDB = volleyBallDatabase(cursor= cursor, connection= connection)

cursor.execute("SELECT practice_id, date FROM vbms.practice ")
dates = cursor.fetchall()

cursor.execute("SELECT practice_id, user_id FROM vbms.attendance WHERE;")
table = cursor.fetchall()

#SELECT now()::timestamp <- gives now w/o timezone

for i in table:

    status = random.randint(1, 3)

    < datetime.now()