import psycopg2
import json
with open('config.json','r') as data:
    config=json.load(data)

connection = psycopg2.connect(**config)

cursor =connection.cursor()

create_announcements="""
    CREATE TABLE IF NOT EXISTS vbms.announcements
    (
        announcement_id integer NOT NULL DEFAULT nextval('vbms.announcements_announcement_id_seq'::regclass),
        publisher_uid integer NOT NULL,
        date_published date,
        content text COLLATE pg_catalog."default",
        CONSTRAINT annnouncements_pkey PRIMARY KEY (announcement_id)
    )
"""
create_users="""
    CREATE TABLE IF NOT EXISTS vbms.users
    (
        uid integer NOT NULL DEFAULT nextval('vbms.users_uid_seq'::regclass),
        email text COLLATE pg_catalog."default",
        uname text COLLATE pg_catalog."default",
        pword text COLLATE pg_catalog."default",
        role text COLLATE pg_catalog."default",
        CONSTRAINT users_pkey PRIMARY KEY (uid)
    )
"""

create_games="""
    CREATE TABLE IF NOT EXISTS vbms.games
    (
        gid integer NOT NULL DEFAULT nextval('vbms.games_gid_seq'::regclass),
        location text COLLATE pg_catalog."default",
        description text COLLATE pg_catalog."default",
        gamedate date,
        CONSTRAINT games_pkey PRIMARY KEY (gid)
    )
"""

cursor.execute("SELECT * FROM vbms.users")
print(cursor.fetchall())