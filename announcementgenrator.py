import csv
import json
from faker import Faker
import random
import datetime
import psycopg2

# Initialize Faker
fake = Faker()

def generate_random_date(start_year, end_year):
    start_date = datetime.datetime(start_year, 1, 1)
    end_date = datetime.datetime(end_year, 12, 31)
    return fake.date_between(start_date=start_date, end_date=end_date)

# Volleyball-specific content
teams = ['Spikers', 'Aces', 'Blockers', 'Diggers', 'Setters', 'Hitters']
tournaments = ['Spring Volleyfest', 'Beach Volleyball Championship', 'Indoor Volley League']
players = ['John Doe', 'Jane Smith', 'Alex Johnson', 'Emily Davis', 'Chris Brown', 'James Gore', 'Anusha', 'Megan']
coaches = ['Coach Anderson', 'Coach Bailey', 'Coach Chen', 'Coach Díaz']
cancellation_reasons = ['due to weather conditions', 'due to unforeseen circumstances', 'as the venue is under maintenance']

# Additional details
team_strengths = {
    'Spikers': 'strong defense',
    'Aces': 'powerful serving',
    'Blockers': 'excellent blocking skills',
    'Diggers': 'quick reflexes',
    'Setters': 'strategic playmakers',
    'Hitters': 'aggressive attacking'
}

common_injuries = ['ankle sprain', 'knee injury', 'shoulder strain', 'back pain']

# Function to create a volleyball-related announcement
def create_volleyball_announcement():

    announcement_type = random.choice([
        'match_preview', 'match_result', 'injury_report', 'transfer_news',
        'special_event', 'training_camp', 'season_summary', 'fan_interaction'
        , 'coach_statement', 'match_cancellation'
    ])
    event_date = generate_random_date(2000, 2023)  # Date of the event
    publish_date = generate_random_date(2000, 2023)  # Date of announcement publication
    location = fake.city()
    coach = random.choice(coaches)
    team_a = random.choice(teams)
    team_b = random.choice([team for team in teams if team != team_a])
    player = random.choice(players)
    injury = random.choice(common_injuries)
    team = random.choice(teams)

    announcement_type = random.choice(['match', 'tournament', 'player'])
    if announcement_type == 'match':
        team_a = random.choice(teams)
        team_b = random.choice(teams)
        while team_b == team_a:
            team_b = random.choice(teams)
        return f"Upcoming match between {team_a} and {team_b} on {fake.date()} {fake.time()}"


    if announcement_type == 'match_preview':
        return (f"Exciting Match Preview: {team_a} vs {team_b} on {event_date} at {location}. "
                f"Coach {coach} comments on strategies and strengths. Star player: {player}.")

    elif announcement_type == 'match_result':
        winning_team = random.choice([team_a, team_b])
        score = f"{random.randint(0, 3)} - {random.randint(0, 3)}"
        return (f"Update: {winning_team} wins with a score of {score}. "
                f"Highlights: exceptional performance by {player}. Coach {coach}'s analysis provided insights.")

    elif announcement_type == 'injury_report':
        return (f"Injury Report: {player} of {team_a} suffered a {injury}. "
                f"Recovery period estimated by medical team. Coach {coach} comments.")

    elif announcement_type == 'transfer_news':
        new_team = random.choice([team for team in teams if team != team_a])
        return (f"Transfer News: {player} moves from {team_a} to {new_team}. "
                f"This significant change is expected to alter team dynamics.")

    elif announcement_type == 'match_cancellation':
        reason = random.choice(cancellation_reasons)
        return (f"Match Cancellation: Match between {team_a} and {team_b} on {event_date} at {location} cancelled {reason}. "
                f"Coach {coach} expresses thoughts.")
    elif announcement_type == 'special_event':
        event_name = random.choice(['Autograph Session', 'Fan Meet-Up', 'Charity Match', 'End-of-Season Gala'])
        return (f"Special Event: Join us for the {event_name} on {event_date} at {location}. "
                f"Meet your favorite players and enjoy a day full of exciting activities!")

    elif announcement_type == 'training_camp':
        camp_topic = random.choice(['Offensive Strategies', 'Defensive Techniques', 'Physical Conditioning', 'Team Building'])
        return (f"Training Camp: {team} announces a {camp_topic} training camp on {event_date} at {location}. "
                f"Open for both new talents and seasoned players!")

    elif announcement_type == 'season_summary':
        season_highlight = random.choice(['winning the championship', 'a remarkable comeback', 'the debut of new players', 'setting a new team record'])
        return (f"Season Summary: Reflecting on a season marked by {season_highlight}, "
                f"coach {coach} shares insights and highlights from the past year.")

    elif announcement_type == 'fan_interaction':
        interaction_type = random.choice(['online Q&A session', 'fan poll', 'social media contest', 'ticket giveaway'])
        return (f"Published on {publish_date} - Fan Interaction: Engage with {team} through our {interaction_type}! "
                f"Check out our social channels for more details and get involved!")

    elif announcement_type == 'coach_statement':
        statement_topic = random.choice(['upcoming season', 'recent match performance', 'team strategy', 'player development'])
        return (f"Coach Statement: Coach {coach} discusses {statement_topic}, "
                f"sharing thoughts and plans for the future of {team}.")

    else:
        return f"General Announcement: Stay tuned for updates and news about upcoming events and matches."

# Read database configuration
with open('config.json', 'r') as data:
    config = json.load(data)

# Connect to the database
connection = psycopg2.connect(**config)
cursor = connection.cursor()

cursor.execute("SELECT user_id FROM vbms.users WHERE (user_id = 'admin' OR user_id = 'coach');")
publisher_uid = cursor.fetchall()

# Number of fake announcements to generate
num_announcements = 1000

# CSV file and writing  the announcements
with open('announcement.csv', mode='w', newline='', encoding="utf-8") as announcement_file:
    write_announcement = csv.writer(announcement_file, delimiter=',', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
    write_announcement.writerow(["announcement_id", "publisher_uid", "date_published", "content"])
    for _ in range(num_announcements):
        announcement = create_volleyball_announcement()
        write_announcement.writerow([announcement])

# Close the connection
cursor.close()
connection.close()
