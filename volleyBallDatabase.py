import psycopg2
import json

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

-- Trigger: after_insert_sets    

-- DROP TRIGGER IF EXISTS after_insert_sets ON vbms.sets()

CREATE OR REPLACE TRIGGER after_insert_sets
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
        self.cursor.execute("SELECT * FROM vbms.games")
        return self.cursor.fetchall()
    
    def fetch_practice(self):
       self.cursor.execute("SELECT * FROM vbms.practice")
       return self.cursor.fetchall()
    
    def fetch_attendance(self):
        self.cursor.execute("SELECT * FROM vbms.attendance")
        return self.cursor.fetchall()
    
    def fetch_announcements(self):
        self.cursor.execute("SELECT * FROM vbms.announcements")
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
        location, description, gamedate, opponent, game_score)
        VALUES ('{location}', '{description}', '{gamedate}', '{opponent}', null);
         """)
         self.connection.commit()
    
    def insert_set(self, set_num, usm_score, opponent_score):
        self.cursur.execute(f"""
        INSET INTO vbms.sets(
         set_num, usm_score, opponent_score)
        VALUES ('{set_num}', '{usm_score}', '{opponent_score}');
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
        SET shirt_size={size}
        WHERE user_id={user_id};
        """)
        self.connection.commit()
    
    def update_user_phone_number(self,user_id,phone_number):
        self.cursor.execute(f"""
        UPDATE vbms.users
        SET phone_num={phone_number}
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
