
#This will be used for communicating with the database then with the web app
from flask import Flask,render_template
# psycopg2 is a library for connecting
import psycopg2
import json

#Database connection
with open('config.json','rb') as data:
    config=json.load(data)

connection = psycopg2.connect(**config)

cursor =connection.cursor()

# Create the Flask app instance
app = Flask(__name__)

# Define a route for the root URL
@app.route('/')
def hello_world():
    return 'Nothing'

# Run the app if this script is executed directly
if __name__ == '__main__':
    app.run(debug=True)