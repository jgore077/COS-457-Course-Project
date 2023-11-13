#Fake User Information Generator
import csv
import json
from faker import Faker #pip install Faker
from volleyBallDatabase import volleyBallDatabase
import psycopg2
fake = Faker()
vbDB = volleyBallDatabase()

with open('config.json','r') as data:
    config=json.load(data)

connection = psycopg2.connect(**config)

cursor =connection.cursor()

#fake.name() <- produces randomized name
