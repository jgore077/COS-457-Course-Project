import psycopg2
import json
with open('config.json','r') as data:
    config=json.load(data)

connection = psycopg2.connect(**config)

cursor =connection.cursor()



cursor.execute("SELECT * FROM vbms.users")
print(cursor.fetchall())