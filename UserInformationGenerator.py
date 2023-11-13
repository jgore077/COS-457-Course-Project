#Fake User Information Generator
import csv
import json
from faker import Faker #pip install Faker
from volleyBallDatabase import volleyBallDatabase
import psycopg2

fake = Faker()


with open('config.json','r') as data:
    config=json.load(data)

connection = psycopg2.connect(**config)
cursor = connection.cursor()
vbDB = volleyBallDatabase(cursor= cursor, connection= connection)

#fake.name() <- produces randomized name

#csv file for users table
user_file = open('user.csv', 'w', newline='', encoding="utf-8")
write_user = csv.writer(user_file, delimiter=',', lineterminator='\n')

i = 0
#Table Users(user_id, email, uname, pword, role, phone_num, is_commuter, shirt_size)
names = [(fake.unique.name()).replace(" ", ".") for i in range(1000)]



user_file.close()