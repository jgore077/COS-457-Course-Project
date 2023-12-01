import psycopg2
import json
import time
from datetime import datetime

create_announcements="""
-- Table: vbms.announcements

-- DROP TABLE IF EXISTS vbms.announcements;

CREATE TABLE IF NOT EXISTS vbms.announcements
(
    announcement_id integer NOT NULL DEFAULT nextval('vbms.announcements_announcement_id_seq'::regclass),
    publisher_uid integer NOT NULL,
    date_published timestamp with time zone,
    content text COLLATE pg_catalog."default",
    CONSTRAINT annnouncements_pkey PRIMARY KEY (announcement_id),
    CONSTRAINT publisher_fkey FOREIGN KEY (publisher_uid)
        REFERENCES vbms.users (user_id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE RESTRICT
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS vbms.announcements
    OWNER to volleyballadmin;
"""
create_users="""
           -- Table: vbms.users

-- DROP TABLE IF EXISTS vbms.users;

CREATE TABLE IF NOT EXISTS vbms.users
(
    user_id integer NOT NULL DEFAULT nextval('vbms.users_uid_seq'::regclass),
    email text COLLATE pg_catalog."default",
    uname text COLLATE pg_catalog."default",
    pword text COLLATE pg_catalog."default",
    role text COLLATE pg_catalog."default",
    phone_num text COLLATE pg_catalog."default",
    is_commuter boolean,
    shirt_size text COLLATE pg_catalog."default",
    CONSTRAINT users_pkey PRIMARY KEY (user_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS vbms.users
    OWNER to volleyballadmin;  
"""

create_games="""
    -- Table: vbms.games

-- DROP TABLE IF EXISTS vbms.games;

CREATE TABLE IF NOT EXISTS vbms.games
(
    game_id integer NOT NULL DEFAULT nextval('vbms.games_gid_seq'::regclass),
    location text COLLATE pg_catalog."default",
    description text COLLATE pg_catalog."default",
    gamedate timestamp with time zone NOT NULL,
    opponent text COLLATE pg_catalog."default",
    match_score text COLLATE pg_catalog."default",
    CONSTRAINT games_pkey PRIMARY KEY (game_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS vbms.games
    OWNER to volleyballadmin;

-- Trigger: update_match_scores_trigger   

-- DROP TRIGGER IF EXISTS update_match_scores_trigger ON vbms.sets()

CREATE OR REPLACE TRIGGER update_match_scores_trigger
AFTER INSERT
ON vbms.sets
FOR EACH ROW
EXECUTE FUNCTION vbms.update_match_score();
"""
create_practices="""
-- Table: vbms.practice

-- DROP TABLE IF EXISTS vbms.practice;

CREATE TABLE IF NOT EXISTS vbms.practice
(
    practice_id integer NOT NULL DEFAULT nextval('vbms."practice _practice_id_seq"'::regclass),
    description text COLLATE pg_catalog."default",
    location text COLLATE pg_catalog."default",
    date timestamp with time zone,
    CONSTRAINT practice_pkey PRIMARY KEY (practice_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS vbms.practice
    OWNER to volleyballadmin;

-- Trigger: add_attendance_rows_trigger

-- DROP TRIGGER IF EXISTS add_attendance_rows_trigger ON vbms.practice;

CREATE OR REPLACE TRIGGER add_attendance_rows_trigger
    AFTER INSERT
    ON vbms.practice
    FOR EACH ROW
    EXECUTE FUNCTION vbms.add_attendance_rows();
"""
create_attendance="""
-- Table: vbms.attendance

-- DROP TABLE IF EXISTS vbms.attendance;

CREATE TABLE IF NOT EXISTS vbms.attendance
(
    practice_id integer NOT NULL,
    user_id integer NOT NULL,
    attendance_status integer,
    CONSTRAINT practice_pkey FOREIGN KEY (practice_id)
        REFERENCES vbms.practice (practice_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT user_fkey FOREIGN KEY (user_id)
        REFERENCES vbms.users (user_id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE RESTRICT
        NOT VALID,
    CONSTRAINT status_check CHECK (attendance_status >= 0 AND attendance_status <= 2) NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS vbms.attendance
    OWNER to volleyballadmin;

COMMENT ON COLUMN vbms.attendance.attendance_status
    IS '0-absent, 1-present, 2-excused';
-- Index: fki_user_fkey

-- DROP INDEX IF EXISTS vbms.fki_user_fkey;

CREATE INDEX IF NOT EXISTS fki_user_fkey
    ON vbms.attendance USING btree
    (user_id ASC NULLS LAST)
    TABLESPACE pg_default;
"""
create_sets="""
-- Table: vbms.sets

-- DROP TABLE IF EXISTS vbms.sets;

CREATE TABLE IF NOT EXISTS vbms.sets
(
    game_id integer NOT NULL,
    set_num integer,
    usm_score integer,
    opponent_score integer,
    CONSTRAINT "game_idFK" FOREIGN KEY (game_id)
        REFERENCES vbms.games (game_id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS vbms.sets
    OWNER to volleyballadmin;
"""

class volleyBallDatabase():

    def __init__(self,cursor,connection) -> None:
        self.cursor=cursor
        self.connection=connection
        
    # ---------------------- SELECT ALLs ----------------------------------
    def fetch_users(self):
        self.cursor.execute("SELECT * FROM vbms.users")
        return self.cursor.fetchall()
    
    def fetch_user(self,username):
        self.cursor.execute(f"SELECT user_id FROM vbms.users WHERE uname='{username}'")
        return self.cursor.fetchall()
    
    def fetch_all_user(self,user_id):
        self.cursor.execute(f"SELECT * FROM vbms.users WHERE user_id={user_id}")
        # This feels like a sin but its probably ok
        return self.cursor.fetchall()

    def fetch_all_username_and_email(self):
        self.cursor.execute("SELECT uname,email FROM vbms.users")
        return self.cursor.fetchall()
    
    def fetch_user_and_role(self,username):
        self.cursor.execute(f"SELECT user_id, role FROM vbms.users WHERE uname='{username}'")
        return self.cursor.fetchall()
    
    def fetch_email(self,email):
        self.cursor.execute(f"SELECT user_id FROM vbms.users WHERE email='{email}'")
        return self.cursor.fetchall()
    
    def fetch_password(self,username):
        self.cursor.execute(f"SELECT pword FROM vbms.users WHERE uname='{username}'")
        return self.cursor.fetchall()
        
    def fetch_games(self):
        self.cursor.execute("""SELECT * FROM vbms.games
            ORDER BY gamedate DESC  """)
        return self.cursor.fetchall()
    
    def fetch_practice(self):
       self.cursor.execute("SELECT * FROM vbms.practice")
       return self.cursor.fetchall()
    
    def fetch_attendance(self):
        self.cursor.execute("SELECT * FROM vbms.attendance")
        return self.cursor.fetchall()
    
    def fetch_announcements(self):
        self.cursor.execute("""SELECT * FROM vbms.announcements 
                            ORDER BY date_published DESC""")
        return self.cursor.fetchall()
    
    def fetch_sets(self):
        self.cursor.execute("SELECT * FROM vbms.sets")
        return self.cursor.fetchall()
    #----------------------------------------- Inserts ----------------------------------------------
    def insert_practice(self,description,location,date):
        self.cursor.execute(f"""
        INSERT INTO vbms.practice(
	    description, location, date)
	    VALUES ('{description}', '{location}', '{date}');
        """)
        self.connection.commit()
        
    def insert_game(self,location,description,gamedate,opponent):
         self.cursor.execute(f"""
        INSERT INTO vbms.games(
        location, description, gamedate, opponent)
        VALUES ('{location}', '{description}', '{gamedate}', '{opponent}');
         """)
         self.connection.commit()
    
    def insert_set(self, game_id, set_num, usm_score, opponent_score):
        self.cursor.execute(f"""
        INSERT INTO vbms.sets(
         game_id, set_num, usm_score, opponent_score)
        VALUES ('{game_id}', '{set_num}', '{usm_score}', '{opponent_score}');
        """)
        self.connection.commit()

    def insert_user(self,email,uname,pword):
        self.cursor.execute(f"""
        INSERT INTO vbms.users(
         email, uname, pword, role, phone_num, is_commuter, shirt_size)
        VALUES ( '{email}', '{uname}', '{pword}', null, null, null, null);
        """)
        self.connection.commit()
        
    def insert_announcement(self,publisher_uid,date_published,content):
        # You need to commit after executing insert or delete querys
        self.cursor.execute(f"INSERT INTO vbms.announcements(publisher_uid, date_published, content) VALUES ({publisher_uid}, '{date_published}', '{content}');")
        self.connection.commit()
    # -------------------------------- User updates ---------------------------------------
    def update_user_shirt_size(self,user_id,size):
        self.cursor.execute(f"""
        UPDATE vbms.users
        SET shirt_size='{size}'
        WHERE user_id={user_id};
        """)
        self.connection.commit()
    
    def update_user_phone_number(self,user_id,phone_number):
        self.cursor.execute(f"""
        UPDATE vbms.users
        SET phone_num='{phone_number}'
        WHERE user_id={user_id};
        """)
        self.connection.commit()
        
    def update_user_commuter_status(self,user_id,isCommuter):
        self.cursor.execute(f"""
        UPDATE vbms.users
        SET is_commuter={isCommuter}
        WHERE user_id={user_id};
        """)
        self.connection.commit()
    # ---------------------------- Practice status ---------------------------
    def update_attendance(self,practice_id,user_id,status):
        self.cursor.execute(f"""
        UPDATE vbms.attendance
        SET attendance_status={status}
        WHERE user_id={user_id} and practice_id={practice_id};
        """)
        self.connection.commit()
    # --------------------------- Update Set Score ----------------------------
    def update_set(self, game_id, set_num, usm_score, opponent_score):
        self.cursor.execute(f"""
        UPDATE vbms.sets
        SET set_num={set_num}, usm_score={usm_score}, opponent_score={opponent_score}
        WHERE game_id={game_id};
        """)
        self.connection.commit()

    def update_game(self,id,location,opponent,description,datetime):
        self.cursor.execute(f"""UPDATE vbms.games
        SET  location='{location}', description='{description}', gamedate='{datetime}', opponent='{opponent}'
        WHERE game_id={id}
        """)
        self.connection.commit()
        
    def update_announcement(self,id,content):
        self.cursor.execute(f"""
        UPDATE vbms.announcements
        SET content='{content}'
        WHERE announcement_id={id};
        """)
        self.connection.commit()
    #--------------------------- Search Functions ------------------
    #------- Basic Table Searches------
    #search announcements
    def search_announcement(self, value):
        query = """
        SELECT *
   	    FROM vbms.announcements
        WHERE 
            CAST(publisher_uid AS VARCHAR) ILIKE %s
            OR CAST(date_published AS VARCHAR) ILIKE %s
            OR content ILIKE %s;
        """
        self.cursor.execute(query, (f"%{value}%",) * 3)
        return self.cursor.fetchall()  
    #search attendance
    def search_attendance(self, value):
        query = """
        SELECT *
        FROM vbms.attendance 
        WHERE 
            CAST(user_id AS VARCHAR) ILIKE %s
            OR CAST(attendance_status AS VARCHAR) ILIKE %s;
        """  
        self.cursor.execute(query, (f"%{value}%",) * 2)
        return self.cursor.fetchall()
    #search games
    def search_games(self, value):
        query = """
        SELECT *
        FROM vbms.games
        WHERE 
            location ILIKE %s
            OR description ILIKE %s
            OR CAST(gamedate AS VARCHAR) ILIKE %s
            OR opponent ILIKE %s
            OR match_score ILIKE %s;
        """
        self.cursor.execute(query, (f"%{value}%",) * 5)
        return self.cursor.fetchall()
    #search practice
    def search_practice(self, value):
        query = """
        SELECT *
        FROM vbms.practice
        WHERE 
            description ILIKE %s
            OR location ILIKE %s
            OR CAST(date AS VARCHAR) ILIKE %s;
        """
        self.cursor.execute(query, (f"%{value}%",) * 3)
        return self.cursor.fetchall()
    #search users
    def search_users(self, value):
        query = """
        SELECT *
        FROM vbms.users
        WHERE 
            CAST(user_id AS VARCHAR) ILIKE %s 
            OR email ILIKE %s 
            OR uname ILIKE %s 
            OR role ILIKE %s 
            OR phone_num ILIKE %s 
            OR CAST(is_commuter AS VARCHAR) ILIKE %s 
            OR shirt_size ILIKE %s;
        """
        self.cursor.execute(query, (f"%{value}%",) * 7)
        return self.cursor.fetchall()

    #------------------------- Complex Searches -------------------
    #Precision Search Functionality
    # This requires specified table and at least one attribute. Can do two attributes and values as well.
    #does not include sets table search as this is not needed
    def precision_search(self, table, attribute1, value1=None, attribute2=None, value2=None):
        # Validate that the provided table and attribute are valid
        valid_tables = ["announcements", "attendance", "games", "practice", "users"]
        valid_attributes = {
            "announcements": ["publisher_uid", "date_published", "content"], #announcement_id not included
            "attendance": ["practice_id", "user_id", "attendance_status"],
            "games": ["location", "description", "gamedate", "opponent", "match_score"],#game_id not included
            "practice": ["practice_id", "description", "location", "date"],
            "users": ["user_id", "email", "uname", "role", "phone_num", "is_commuter", "shirt_size"], #pword not included
        }
        #if provided table/attribute not valid, raise error
        if table not in valid_tables:
            raise ValueError(f"Invalid table: {table}. Valid tables are {valid_tables}")
        if attribute1 not in valid_attributes.get(table, []):
            raise ValueError(f"Invalid attribute for table {table}: {attribute1}. Valid attributes are {valid_attributes.get(table, [])}")
        if attribute2 is not None and attribute2 not in valid_attributes.get(table, []):
            raise ValueError(f"Invalid second attribute for table {table}: {attribute2}. Valid attributes are {valid_attributes.get(table, [])}")
        
        table_name = 'vbms.' + table
        value1 = self.cast_value(attribute1, value1) #make sure value1 matches data type of attribute1
        if attribute2 is not None:
            if value2 is not None:
                query = f"SELECT * FROM {table_name} WHERE {attribute1} = %s AND {attribute2} = %s;"
                value2 = self.cast_value(attribute2, value2)
                self.cursor.execute(query, (value1, value2))
            else:#if value2 is left blank but we have specified 2 valid attributes, it will search each attribute using value1 for both.
                query = f"SELECT * FROM {table_name} WHERE {attribute1} = %s AND {attribute2} = %s;"
                value2 = self.cast_value(attribute2, value1)#returns value1 as the data type of attribute2
                self.cursor.execute(query, (value1, value2))
        else:
            query = f"SELECT * FROM {table_name} WHERE {attribute1} = %s;"
            self.cursor.execute(query, (value1,))
        return self.cursor.fetchall()
    
    #casting method for searches
    def cast_value(self, attribute, value, date_format="%Y-%m-%d %H:%M:%S"):
        if attribute in ["date_published", "date", "gamedate"]:
            try:
                if " " in value:  # Check if there's a space in the value, indicating both date and time
                    return datetime.strptime(value, date_format)
                else:
                    return datetime.strptime(value, "%Y-%m-%d").replace(hour=0, minute=0, second=0)
                ### EDIT needed, this will only search at time 0:0:0 if no time specified for date, need to fix this
            except ValueError:
                # Handle the case where the string is not in the expected format
                raise ValueError(f"Error: Unable to parse {value} to datetime using format {date_format}")
        elif attribute in ["is_commuter"]:
            return value.lower() in ['true', 'yes'] #will accept TRUE, True, YeS, etc. false if anything else
        elif attribute in ["user_id", "publisher_uid", "practice_id"]:
            try:
                return int(value)# Attempt to cast the string to an integer
            except ValueError:
                raise ValueError(f"Error: Unable to cast {value} to integer for attribute {attribute}")
        elif attribute in ["attendance_status"]:
            if str(value).lower() in ["2", "present", "two"]:
                return 2
            elif str(value).lower() in ["1", "excuse", "excused", "one"]:
                return 1
            elif str(value).lower() in ["0", "absent", "zero"]:
                return 0
            else:
                raise ValueError(f"Error: Invalid entry, {value}, for attribute {attribute}. 2-present, 1-excused, 0-absent")
        else:
            return str(value) #returns value as string
    
    #Broad Search Functionality
    #allows user to input a string value to search by and returns results from all tables
    def broad_search(self, value):
        announcements_results = self.search_announcement(value)
        attendance_results = self.search_attendance(value)
        games_results = self.search_games(value)
        practice_results = self.search_practice(value)
        users_results = self.search_users(value)
        return [announcements_results, attendance_results, games_results, practice_results, users_results]

    def format_row(self, row):
        """
        Formatting the row with the specified pattern
        """
        return {'game_id': row[0], 'location': row[1], 'gamedate': row[3].strftime("%Y-%m-%d %H:%M:%S"),'description':row[2],'opponent':row[4],'game_score':row[5]}
    
    #Match Search functionality 
    def search_matches(self, date=None, location=None):
        query = """
        SELECT g.*
        FROM vbms.games g
        WHERE (%s IS NULL OR g.gamedate = %s)
          AND (%s IS NULL OR g.location ILIKE %s);
        """
        self.cursor.execute(query, (date, date, location, f'%{location}%'))
        results = [self.format_row(row) for row in self.cursor.fetchall()]
        
        return results
    
    
    #Follow this format for the matches {'id':row[0],'description':row[3],'datetime':row[2].strftime("%Y-%m-%d %H:%M:%S")}
    #News Search Functionality 
    def search_news(self, date_published=None, content=None):
       
        query = """
        SELECT announcement_id, publisher_uid, date_published, content
        FROM vbms.announcements
        WHERE (%s IS NULL OR date_published::date = %s::date)
          AND (%s IS NULL OR content ILIKE %s);
        """
        self.cursor.execute(query, (date_published, date_published, content, f'%{content}%'))
        
        results = [self.format_row(row) for row in self.cursor.fetchall()]

        return results
    
if __name__=="__main__":
    with open('config.json','r') as data:
        config=json.load(data)

    connection = psycopg2.connect(**config)

    cursor =connection.cursor()
    db = volleyBallDatabase(cursor=cursor,connection=connection)
    
    # t1 =time.time()
    # print(db.search_news(content='Match Cancel'),end='\n\n')
    # t2 =time.time()
    
    
    t3 =time.time()
    print(db.search_matches(location='University Of'),end='\n\n')
    t4 =time.time()

    # t5=time.time()
    # print(db.search_news(date_published='2011-03-02'),end='\n\n')
    # t6=time.time()
    
    # print(f'News search took with date: {t6-t5} seconds \n')
    
    # print(f'Match search took: {t4-t3} seconds \n')
    # #testing precision_search
    # print(db.precision_search('users', 'role', 'coach'))
    # #testing broad_search
    # print(db.broad_search(["megan.fleck@maine.edu"]))