import csv
import json
import random
from faker import Faker # Installation: pip install Faker
from volleyBallDatabase import volleyBallDatabase
import psycopg2 # Installation: pip install psycopg2

# Initialize Faker
fake = Faker()

#csv file for users table
user_file = open('user.csv', 'w', newline='', encoding="utf-8")
write_user = csv.writer(user_file, delimiter=',', lineterminator='\n')
write_user.writerow(["user_id", "email", "uname", "pword", "role", "phone_num", "is_commuter", "shirt_size"])
#Table Users("user_id", "email", "uname", "pword", "role", "phone_num", "is_commuter", "shirt_size")

#Adding a specific admin user
write_user.writerow(["1078735", "megan.fleck@maine.edu", "megan.fleck", "password123", "admin", "2078075832", "TRUE", "M"])

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

# Generate user names in format "firstName.last.Name" not neccessarily unique
uname = [(fake.name()).replace(" ", ".") for i in range(999)]

# Generate passwords not neccessarily unique
pword = [(fake.word() + str(random.randint(0, 999))) for i in range(999)]

# Generate phone numbers not neccessarily unique
phone_num = [fake.phone_number() for i in range(999)]

role = "player"
# all these users are being entered as players
count = 0
for i in user_id_set:
    is_commuter = random.choice([True, False])
    shirt_size = random.choice(["XS", "S", "M", "L", "XL"])
    write_user.writerow([i, uname[count] + "@maine.edu", uname[count], pword[count], role, phone_num[count], is_commuter, shirt_size])
    count += 1

user_file.close()

# Using the CSV file created above, 'user.csv', we will input this data into our 'users' Table in PostgreSQL

with open('config.json', 'r') as data:
    config = json.load(data)

connection = psycopg2.connect(**config)
cursor = connection.cursor()
vbDB = volleyBallDatabase(cursor= cursor, connection= connection)

csv_file_path = './user.csv'

with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    header = next(csv_reader)

    insert_query = f"INSERT INTO vbms.users VALUES ({', '.join(['%s'] * len(header))})"
    
    # Iterate through each row and execute the insert to the table
    for row in csv_reader:
        cursor.execute(insert_query, row)

connection.commit()
cursor.close()
connection.close()