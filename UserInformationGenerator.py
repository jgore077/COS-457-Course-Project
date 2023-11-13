#Fake User Information Generator
import csv
import json
import random
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
write_user.writerow(["user_id", "email", "uname", "pword", "role", "phone_num", "is_commuter", "shirt_size"])
#Table Users("user_id", "email", "uname", "pword", "role", "phone_num", "is_commuter", "shirt_size")

#Adding a specific admin user
write_user.writerow(["1078735", "megan.fleck@maine.edu", "megan.fleck", "password123", "coach", "2078075832", "TRUE", "M"])

def generate_unique_integers(length, count):
    lower_bound = 10 ** (length - 1)
    upper_bound = (10 ** length) - 1

    #Ensure uniqueness using a set
    unique_numbers = set()

    while len(unique_numbers) < count:
        unique_numbers.add(random.randint(lower_bound, upper_bound))

    return list(unique_numbers)

# Generate unique user IDs of length 7 (unique)
user_id_set = generate_unique_integers(7, 999)
print("num of User IDs: " + str(len(user_id_set)))

# Generate user names in format "firstName.last.Name" not neccessarily unique
uname = [(fake.name()).replace(" ", ".") for i in range(999)]
print("num of User names: " + str(len(uname)))

# Generate passwords not neccessarily unique
pword = [(fake.word() + str(random.randint(0, 999))) for i in range(999)]
print("num of passwords: " + str(len(pword)))

# Generate phone numbers not neccessarily unique
phone_num = [fake.phone_number() for i in range(999)]
print("num of Phone Numbers: " + str(len(phone_num)))

role = "player"
# all these users are being entered as players
count = 0
for i in user_id_set:
    is_commuter = random.choice([True, False])
    shirt_size = random.choice(["XS", "S", "M", "L", "XL"])
    write_user.writerow([i, uname[count] + "@maine.edu", uname[count], pword[count], role, phone_num[count], is_commuter, shirt_size])
    count += 1

user_file.close()