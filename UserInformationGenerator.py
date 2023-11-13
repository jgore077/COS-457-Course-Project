import csv
import json
import random
from faker import Faker # Installation: pip install Faker
from volleyBallDatabase import volleyBallDatabase
import psycopg2 # Installation: pip install psycopg2

fake = Faker()

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

# Using the CSV file created above, 'user.csv', we will infput this data into our 'users' Table in PostgreSQL

with open('config.json','r') as data:
    config=json.load(data)

connection = psycopg2.connect(**config)
cursor = connection.cursor()
vbDB = volleyBallDatabase(cursor= cursor, connection= connection)


csv_file_path = '\Users\Megan Fleck\COS-457-Course-Project\user.csv'

with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    header = next(csv_reader)

    # Iterate through each row and execute the insert to the table
    for row in csv_reader:
        current_row = row.split(',')
        user_id = current_row[0]
        cursor.execute("INSERT INTO {vbms.users} VALUES ('{current_row[0]}', '{current_row[1]}', '{current_row[2]}', '{current_row[3]}', '{current_row[4]}', '{current_row[5]}', '{current_row[6]}', '{current_row[7]}')")

connection.commit()
cursor.close()
connection.close()
