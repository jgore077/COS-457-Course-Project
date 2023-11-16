import csv
import json
from faker import Faker
import random
import psycopg2

# Initialize Faker
fake = Faker()

# Volleyball-specific content
teams = ['Spikers', 'Aces', 'Blockers', 'Diggers', 'Setters', 'Hitters']
tournaments = ['Spring Volleyfest', 'Beach Volleyball Championship', 'Indoor Volley League']
players = ['John Doe', 'Jane Smith', 'Alex Johnson', 'Emily Davis', 'Chris Brown', 'James Gore', 'Anusha', 'Megan']

# Function to create a volleyball-related announcement
def create_volleyball_announcement():
    announcement_type = random.choice(['match', 'tournament', 'player'])
    if announcement_type == 'match':
        team_a = random.choice(teams)
        team_b = random.choice(teams)
        while team_b == team_a:
            team_b = random.choice(teams)
        return f"Upcoming match between {team_a} and {team_b} on {fake.date()} {fake.time()}"

    elif announcement_type == 'tournament':
        tournament = random.choice(tournaments)
        return f"Join us for the {tournament} starting {fake.date()}"

    elif announcement_type == 'player':
        player = random.choice(players)
        return f"Spotlight on player: {player}"


with open('config.json', 'r') as data:
    config = json.load(data)

connection = psycopg2.connect(**config)
cursor = connection.cursor()

# number of fake announcements to generate
num_announcements = 500

# Open a CSV file 
announcement_file = open('announcement.csv', 'w', newline='', encoding="utf-8")
write_announcement = csv.writer(announcement_file, delimiter=',', lineterminator='\n')

#  fake announcements
for _ in range(num_announcements):
    announcement = create_volleyball_announcement()
    write_announcement.writerow([announcement])

announcement_file.close()
