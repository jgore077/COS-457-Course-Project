import csv
import json
from faker import Faker
import random
import psycopg2

# Initialize Faker
fake = Faker()

# Function to create a unique username
def create_unique_username(existing_usernames):
    username = f"{fake.user_name()}{random.randint(1, 999)}"
    while username in existing_usernames:
        username = f"{fake.user_name()}{random.randint(1, 999)}"
    return username

with open('config.json', 'r') as data:
    config = json.load(data)

connection = psycopg2.connect(**config)
cursor = connection.cursor()

# number of fake usernames to generate
num_usernames = 1000

# CSV file to store fake usernames
user = open('user.csv', 'w', newline='', encoding="utf-8")
write_username = csv.writer(user, delimiter=',', lineterminator='\n')

# Generate and store fake usernames
existing_usernames = set()
for _ in range(num_usernames):
    username = create_unique_username(existing_usernames)
    existing_usernames.add(username)
    write_username.writerow([username])

user.close()
