import psycopg2
import json



create_announcements="""

"""
create_users="""
 
"""

create_games="""
    
"""
create_practices="""

"""
create_attendance="""

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
        location, description, gamedate, opponent, game_score, set_scores)
        VALUES ('{location}', '{description}', '{gamedate}', '{opponent}', null, null);
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
        
