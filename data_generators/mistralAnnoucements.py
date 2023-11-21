import requests
import json
import random
import csv
from datetime import datetime,timedelta
# YOU WILL NOT BE ABLE TO RUN THIS FILE WITHOUT OLLAMA BUT IT IS INCLUDED FOR TRANSPARENCY
volleyball_locations = [
    "Indoor Sports Complex",
    "Beach Volleyball Court",
    "High School Gymnasium",
    "College Arena",
    "Community Center",
    "Recreational Park",
    "Volleyball Club Facility",
    "Outdoor Sand Court",
    "Sports Stadium",
    "Local YMCA",
    "University Sports Center",
    "Sports and Recreation Center",
    "School Sports Hall",
    "Beach Resort",
    "Public Beach",
    "Hotel Resort Court",
    "Backyard Court",
    "Cruise Ship Deck",
    "Waterfront Park",
    "Campus Recreational Center",
]
days_of_the_week = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday"
]
players = ['John Doe', 'Jane Smith', 'Alex Johnson', 'Emily Davis', 'Chris Brown', 'James Gore', 'Anusha', 'Megan']
announcements = [
    "Team, great practice yesterday! Keep up the hard work and dedication.",
    f"Reminder: Our next match is this {random.choice(days_of_the_week)} at {random.choice(range(1,12))} PM. Be prepared and arrive early.",
    "Let's focus on improving our serving accuracy during this week's practice.",
    f"Congratulations to {random.choice(players)} for earning Player of the Match in our last game!",
    f"Team meeting tomorrow at {random.choice(range(1,12))} PM to discuss strategy and game plan.",
    "We need volunteers for the upcoming fundraiser event. Please sign up if you can help.",
    f"Injury update: {random.choice(players)} is recovering well and should be back on the court soon.",
    "Don't forget to stay hydrated and get plenty of rest before the big tournament this weekend.",
    "Positive attitude and good sportsmanship are crucial. Let's show respect to our opponents.",
    "Shoutout to our amazing fans for their support during our recent home game!",
    "New team jerseys are in! You can pick them up at practice tomorrow.",
    "Coaches have some new drills to help us improve our blocking technique.",
    "Congratulations, team! We've secured a spot in the playoffs. Keep pushing hard!",
    f"Reminder: Team bonding event this  {random.choice(days_of_the_week)} at {random.choice(volleyball_locations)}. It's going to be a blast!",
    "Let's review the scouting report for our next opponent during our film session.",
    "Stay focused on our goals, and remember that we win as a team and lose as a team.",
    f"Happy birthday to {random.choice(players)}! Let's celebrate after practice today.",
    "Captain's challenge: Bring a motivational quote to share at practice tomorrow!",
    "Please let me know if you have any concerns or suggestions to improve our team.",
    "Thank you for your dedication and hard work, team. Together, we can achieve greatness!"
]
with open('volleyball_announcements2.csv', mode='w', newline='',encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)

    # Generate and write 50 rows of data
    for i in range(50):
        response = requests.request(url='http://127.0.0.1:11434/api/generate', method='POST',
                                    data=json.dumps({
                                        "model": "mistral",
                                        "prompt": f"Write an announcement for a volleyball team and use random names when a name is required. It is about {random.choice(announcements)} (NO emojis and NO NEWLINE CHARACTERS)"}))
        responses = response.content.decode('utf-8').strip().split('\n')

        # Extract the 'response' field from each response JSON and join them with spaces
        concatenated_response = ''.join([json.loads(response)['response'] for response in responses])

        # Generate a random datetime within a range (e.g., 30 days ago to now)
        end_datetime = datetime.now()
        start_datetime = end_datetime - timedelta(days=30)
        random_datetime = start_datetime + timedelta(seconds=random.randint(0, int((end_datetime - start_datetime).total_seconds())))

        # Format the random datetime
        formatted_datetime = random_datetime.strftime("%Y-%m-%d %H:%M:%S")

        # Write the data to the CSV file
        writer.writerow([formatted_datetime, concatenated_response.replace('\n','')])