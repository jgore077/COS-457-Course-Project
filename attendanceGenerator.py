import json
import random
from volleyBallDatabase import volleyBallDatabase
import psycopg2 # Installation: pip install psycopg2

with open('config.json', 'r') as data:
    config = json.load(data)

connection = psycopg2.connect(**config)
cursor = connection.cursor()
vbDB = volleyBallDatabase(cursor= cursor, connection= connection)

cursor.execute("SELECT practice_id, user_id FROM vbms.attendance WHERE practice_id IN (SELECT practice_id FROM vbms.practice WHERE date < NOW());")
table = cursor.fetchall()

#SELECT now()::timestamp <- gives now w/o timezone
for row in table:
    status = random.randint(0, 2)
    vbDB.update_attendance(row[0], row[1], status)
    #cursor.execute("INSERT INTO vbms.attendance(attendance_status) VALUES ({status}) WHERE practice_id = {table[row]} AND user_id = {table[row + 1]}")

#cursor.commit()
cursor.close()
connection.close()