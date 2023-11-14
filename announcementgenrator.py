import csv
import json
from faker import Faker
import psycopg2

# Initialize Faker
fake = Faker()

with open('config.json', 'r') as data:
    config = json.load(data)

connection = psycopg2.connect(**config)
cursor = connection.cursor()

# number of fake announcements to generate
num_announcements = 50

# CSV file to store fake announcement data
announcement_file = open('announcement.csv', 'w', newline='', encoding="utf-8")
write_announcement = csv.writer(announcement_file, delimiter=',', lineterminator='\n')

# Generatinng fake announcements
for _ in range(num_announcements):
    title = fake.sentence(nb_words=6)  # fake title
    description = fake.text(max_nb_chars=200)  # fake description
    date = fake.date()  # Generating a fake date
    # Writing to CSV or insert into database
    write_announcement.writerow([title, description, date])

announcement_file.close()
