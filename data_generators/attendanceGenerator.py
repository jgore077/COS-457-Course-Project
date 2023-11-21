import json
import random
from volleyBallDatabase import volleyBallDatabase
import psycopg2 # Installation: pip install psycopg2

# There is a trigger that when a new practice is added, a new row is created for each user for that corresponding practice in the attendance table.
# The default value for status is 0, which means 'absent'. This code will update the status for the previously generated data
# for any practice that happened prior to today, the status 0, 1, or 2 will be randomly chosen for each user. 

with open('config.json', 'r') as data:
    config = json.load(data)

connection = psycopg2.connect(**config)
cursor = connection.cursor()
vbDB = volleyBallDatabase(cursor= cursor, connection= connection)

cursor.execute("SELECT practice_id, user_id FROM vbms.attendance WHERE practice_id IN (SELECT practice_id FROM vbms.practice WHERE date < NOW());")
table = cursor.fetchall()

for row in table:
    status = random.randint(0, 2)
    vbDB.update_attendance(row[0], row[1], status)

cursor.close()
connection.close()