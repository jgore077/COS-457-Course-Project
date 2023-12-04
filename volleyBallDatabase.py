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
    
    def fetch_vectorized_tables(self):
        self.cursor.execute("SELECT * FROM vbms.vectorized_tables")
        return self.cursor.fetchall()
    
    def fetch_all_entrys_from_ids(self,table,list_of_ids):
        
        if list_of_ids==[]:
            return []
        
        table_id_enum={
            'games':'game_id',
            'practice':'practice_id',
            'announcements':'announcement_id'
        }
        self.cursor.execute(f"""SELECT * 
                            FROM vbms.{table}
                            WHERE {table_id_enum[table]} in ({str(list_of_ids).strip('[]')})
                            """)
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
        
    def insert_vectorized_entry(self,origin_id,origin_table,vector):
        self.cursor.execute(f"""INSERT INTO vbms.vectorized_tables(
	        origin_id, origin_table, vector)
	        VALUES ({origin_id}, '{origin_table}', '{vector}');""")
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
    # This requires specified table, at least one attribute and value. Can do two attributes and values as well.
    #does not include sets table search as this is not needed
    def precision_search(self, table, attribute1, value1, attribute2=None, value2=None):
        # Validate that the provided table and attribute are valid
        valid_tables = ["announcements", "attendance", "games", "practice", "users"]
        valid_attributes = {
            "announcements": ["publisher_uid", "date_published", "content"], #announcement_id not included
            "attendance": ["practice_id", "user_id", "attendance_status"],
            "games": ["location", "description", "gamedate", "opponent", "match_score"],#game_id not included
            "practice": ["practice_id", "description", "location", "date"],
            "users": ["user_id", "email", "uname", "role", "phone_num", "is_commuter", "shirt_size"], #pword not included
        }
        #if provided table/attribute not valid, or no value given, then raise error
        if table not in valid_tables:
            raise ValueError(f"Invalid table: {table}. Valid tables are {valid_tables}")
        if attribute1 not in valid_attributes.get(table, []):
            raise ValueError(f"Invalid attribute for table {table}: {attribute1}. Valid attributes are {valid_attributes.get(table, [])}")
        if attribute2 is not None and attribute2 not in valid_attributes.get(table, []):
            raise ValueError(f"Invalid second attribute for table {table}: {attribute2}. Valid attributes are {valid_attributes.get(table, [])}")
        if value1 is None:
            raise ValueError(f"Please enter a value to search by.")
        
        table_name = 'vbms.' + table
        value1 = '%' + str(value1) + '%' 
        if value2 is not None:
            value2 = '%' + str(value2) + '%'
            if attribute2 is not None:
                query = f"SELECT * FROM {table_name} WHERE CAST({attribute1} AS VARCHAR) ILIKE %s AND CAST({attribute2} AS VARCHAR) ILIKE %s"
            else: #attribute2 not specified, but value2 is specified. So search for both values in attribute1
                query = f"SELECT * FROM {table_name} WHERE CAST({attribute1} AS VARCHAR) ILIKE %s AND CAST({attribute1} AS VARCHAR) ILIKE %s"
            self.cursor.execute(query, (value1, value2))
        else: #no value2 specified
            query = f"SELECT * FROM {table_name} WHERE CAST({attribute1} AS VARCHAR) ILIKE %s"
            self.cursor.execute(query, (value1,))
        return self.cursor.fetchall()
    
    #Broad Search Functionality
    #allows user to input a string value to search by and returns results from all tables
    def broad_search(self, value):
        value = '%' + str(value) + '%'
        announcements_results = self.search_announcement(value)
        attendance_results = self.search_attendance(value)
        games_results = self.search_games(value)
        practice_results = self.search_practice(value)
        users_results = self.search_users(value)
        return [announcements_results, attendance_results, games_results, practice_results, users_results]

    #  method for formatting match rows
    def format_match_row(self, row):
        return {
            'game_id': row[0],
            'location': row[1],
            'gamedate': row[3].strftime("%Y-%m-%d %H:%M:%S"),
            'description': row[2],
            'opponent': row[4],
            'game_score': row[5]
        }

    # method for formatting news rows
    def format_news_row(self, row):
        return {
            'id': row[0],
            'description': row[3],
            'datetime': row[2].strftime("%Y-%m-%d %H:%M:%S")
        }

    
    #Match Search functionality 
    def search_matches(self, date=None, location=None):
        date_string=None
        if date:
            date_string=datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d %H:%M:%S')
        query = """
        SELECT g.*
        FROM vbms.games g
        WHERE (%s IS NULL OR g.gamedate = %s)
          AND (%s IS NULL OR g.location ILIKE %s);
        """
        self.cursor.execute(query, (date_string, date_string, location, f'%{location}%'))
        results = [self.format_match_row(row) for row in self.cursor.fetchall()]
        
        return results
    
    #News Search Functionality 
    def search_news(self, date_published=None, content=None):
        date_string=None
        if date_published:
            date_string=datetime.strptime(date_published, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d %H:%M:%S')
        query = """
        SELECT announcement_id, publisher_uid, date_published, content
        FROM vbms.announcements
        WHERE (%s IS NULL OR date_published::date = %s::date)
          AND (%s IS NULL OR content ILIKE %s);
        """
        self.cursor.execute(query, (date_published, date_published, content, f'%{content}%'))
        
        results = [self.format_news_row(row) for row in self.cursor.fetchall()]

        return results
    
    #Implementing join operation on games and sets tables #Project part 3 Search functionality no 2 
    def get_game_and_set_details(self):
     query = """
     SELECT g.game_id, g.location, g.description, g.gamedate, g.opponent, 
            s.set_num, s.usm_score, s.opponent_score
     FROM vbms.games g
     JOIN vbms.sets s ON g.game_id = s.game_id;
        """
     self.cursor.execute(query)
     return self.cursor.fetchall()
    
    #here i am using the EXPLAIN statement to get the query plan
    def explain_game_and_set_details_query_plan(self):
        explain_query = """
        EXPLAIN
        SELECT g.game_id, g.location, g.description, g.gamedate, g.opponent, 
               s.set_num, s.usm_score, s.opponent_score
        FROM vbms.games g
        JOIN vbms.sets s ON g.game_id = s.game_id;
        """
        self.cursor.execute(explain_query)
        return self.cursor.fetchall()
    
    #Functionality for transaction. this function will try to update a new email and check if the email is existing one or not 
    def update_user_email(self, user_id, new_email):
     try:
        # Start a transaction block
        self.connection.autocommit = False #Disabling autocommit for atomic operation, allowing rollback in case of an error.
        
        # Checking if user_id exists
        self.cursor.execute("SELECT * FROM vbms.users WHERE user_id = %s", (user_id,))
        if not self.cursor.fetchone():
            raise ValueError("User ID does not exist")
        
        # Check if the new email already exists
        self.cursor.execute("SELECT * FROM vbms.users WHERE email = %s", (new_email,))
        if self.cursor.fetchone():
            raise ValueError("Email already in use")

        # Update the email if it doesn't exist
        self.cursor.execute("UPDATE vbms.users SET email = %s WHERE user_id = %s", (new_email, user_id))

        # Commit the transaction
        self.connection.commit()
        print("Email updated successfully")

     except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error in transaction: {error}")
        self.connection.rollback()  # Rollback the transaction
        print("Transaction rolled back!")
        raise

     finally:
       self.connection.autocommit = True 

    #this method will test the update_user_email above. it will send a uder_id and new/ already existing email 
    def test_update_user_email(self):
        user_id = 1053941  # will replace with a valid user_id
        new_email = "panianijholmomos@maine.edu"  # will replace this with a new email 
        duplicate_email = "tranquilvibes1923@gmail.com"  # will replace this with somebody's current email

        print("Testing successful email update...")
        try:
            self.update_user_email(user_id, new_email)#use either new_email or duplicate email 
            print(f"Success!User ID {user_id}'s email is successfully be updated to {new_email}")
        except Exception as e:
            print(f"Failed!User ID {user_id}'s email could not be updated to {new_email}.")

    
if __name__=="__main__":
    with open('config.json','r') as data:
        config=json.load(data)

    connection = psycopg2.connect(**config)

    cursor =connection.cursor()
    db = volleyBallDatabase(cursor=cursor,connection=connection)

    #db.test_update_user_email()#testing for project part 3 transaction  
    
    #t1 =time.time()
   # print(db.search_news(content='Match Cancel'),end='\n\n')
    # t2 =time.time()

    
    #t3 =time.time()
    #print(db.search_matches(location='University Of'),end='\n\n')
   # t4 =time.time()

    #t5=time.time()
    #print(db.search_news(date_published='2011-03-02'),end='\n\n')
    #t6=time.time()
    
    # print(f'News search took with date: {t6-t5} seconds \n')
    
    # print(f'Match search took: {t4-t3} seconds \n')
    # #testing precision_search
    #print(db.precision_search('games', 'gamedate', '2024-09-28'))
    # #testing broad_search
    #print(db.broad_search(["megan"]))

    #Testing join queries Project part 3 
    plan = db.explain_game_and_set_details_query_plan()

    for step in plan:
        print(step)
    #print(db.fetch_all_entrys_from_ids('games',[101, 100, 99, 98, 97, 96, 95, 94, 93, 92, 91, 90, 89, 85, 84, 83, 80, 79, 77, 76, 73, 72, 71, 69, 68, 66, 65, 64, 63, 61, 60, 59, 58, 57, 56, 55, 54, 53, 50, 49, 48, 47, 46, 42, 39, 38, 37, 36, 34, 33, 30, 29, 28, 27, 26, 22, 20, 19, 18, 17, 16, 15, 14, 13, 11, 10, 8, 7, 6, 5, 4, 3]))
# vectorized_data=db.fetch_vectorized_tables()
# vector_table_dict=dict()
# for entry in vectorized_data:
#     if entry[1] not in vector_table_dict.keys():
#         vector_table_dict[entry[1]]= [entry]
#         continue
#     vector_table_dict[entry[1]].append(entry)
# print(vector_table_dict['games'])

