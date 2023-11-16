
#This will be used for communicating with the database then with the web app
from flask import Flask,make_response,request,jsonify
# psycopg2 is a library for connecting
import psycopg2
import json
from jwt import InvalidSignatureError,DecodeError,decode,encode
import re
from datetime import datetime
from volleyBallDatabase import volleyBallDatabase
#Database connection

email_regex=re.compile(r"^[A-Za-z0-9._+\-\']+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$")

with open('private.key','r') as data:
    secret=data.read()
with open('config.json','r') as data:
    config=json.load(data)

connection = psycopg2.connect(**config)

cursor =connection.cursor()
db = volleyBallDatabase(cursor=cursor,connection=connection)
# Create the Flask app instance
app = Flask(__name__)

def jwt_auth(jwt_token)->dict:
    try:
        return(decode(jwt_token,secret,algorithms=["HS256"]))
    except (InvalidSignatureError,ValueError,DecodeError) as exception:
        print(exception)
        return {}

def encode_jwt(preEncoded_dict)->str:
    return encode(preEncoded_dict,secret, algorithm="HS256",headers={
        "alg": "HS256",
        "typ": "JWT"
    })

@app.route('/login', methods=["POST"])
def login():
    username=request.json['username']
    password=request.json['password']
    # If it doesnt satisfy conditions return the code as 400
    body={'username':None,'password':None}
    fetchedUsername=db.fetch_user(username)
    print(fetchedUsername)
    res= make_response(json.dumps(body), 200)
    
    user_and_role=db.fetch_user_and_role(username)
    if not fetchedUsername:
        body['username']='Username does not exist'
        
    elif db.fetch_password(username)[0][0]==password:
        res.set_cookie('authToken',encode_jwt({'uid':user_and_role[0][0],'role':user_and_role[0][1]}))
        return res
       
    body['password']='Incorrect Password'

    return make_response(json.dumps(body), 200)
    

@app.route('/signup', methods=["POST"])
def signup():
   
    body={'email':None,'username':None,'password':None}
    
    print(json.dumps(body))
    print(request.json)
    
    email=request.json['email']
    username=request.json['username']
    password=request.json['password']
    if not re.fullmatch(email_regex,email):
        body['email']='Email Invalid'
    elif db.fetch_email(email):
        body['email']='Email Taken'
    
    if len(username)>30:
        body['username']='Username Too Long'
    elif len(username)<6:
        body['username']='Username Too Short Or Empty'
    elif db.fetch_user(username):
        body['username']='Username is taken'
        
    if len(password)<6:
        body['password']='Password Too Weak Or Empty'

    res= make_response(json.dumps(body),200)
    for error in list(body.values()):
        if bool(error):
            return res
        
    db.insert_user(email,username,password)
    user_and_role=db.fetch_user_and_role(username)
    res.set_cookie('authToken',encode_jwt({'uid':user_and_role[0][0],'role':user_and_role[0][1]}))
    return res

# @app.route('/userinfo')
# def getinfo():
#     res=make_response()
#     res.status_code=204
#     print(request.cookies['authToken'])
#     # I need to check if I can validate a jwt token from the client side
#     authed_token=jwt_auth(request.cookies['authToken'])
#     if(authed_token!={}):
  
#         res.status_code=200
#         #load the user data in the data to this
#         res.data= json.dumps({'uid':authed_token['uid']})
#         print('here')
        

#     return res
# add code incase the authToken is invalid
@app.route('/decode',methods=["POST"])
def decodeAuthToken():
    res=make_response()
    res.status_code=204

    token=request.json['authToken']
    decodedToken=jwt_auth(token)
    if(decodedToken!={}):
        
        res.status_code=200
        res.data= json.dumps(decodedToken)
        
        return res
    return res

@app.route('/players')
def players():
    users_and_emails_list=[]
    users_and_emails =db.fetch_all_username_and_email()
    print(users_and_emails)
    for row in users_and_emails:
        users_and_emails_list.append({'username':row[0],'email':row[1]})
    print(users_and_emails_list)
    return make_response(json.dumps({'players':users_and_emails_list}),200)
# Run the app if this script is executed directly

@app.route('/games')
def games():
    games_list=[]
    games =db.fetch_games()

    for row in games:
        games_list.append({'game_id':row[0],'location':row[1],'description':row[2],'gamedate':row[3].strftime("%Y-%m-%d %H:%M:%S"),'opponent':row[4],'game_score':row[5]})
    return make_response(json.dumps({'games':games_list}),200)

@app.route('/creategame')
def creategame():
    pass

@app.route('/createpractice')
def createpractice():
    pass

@app.route('/updategame')
def updategame():
    pass

@app.route('/updatepractice')
def updatepractice():
    pass

if __name__ == '__main__':
    app.run(debug=True)
 