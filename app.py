
#This will be used for communicating with the database then with the web app
from flask import Flask,make_response,request,jsonify
# psycopg2 is a library for connecting
import psycopg2
import json
from jwt import InvalidSignatureError,DecodeError,decode,encode

#Database connection

with open('private.key','r') as data:
    secret=data.read()
with open('config.json','r') as data:
    config=json.load(data)

connection = psycopg2.connect(**config)

cursor =connection.cursor()

# Create the Flask app instance
app = Flask(__name__)

def jwt_auth(jwt_token)->dict:
    try:
        return(decode(jwt_token,secret,algorithms=["HS256"]))
    except (InvalidSignatureError,ValueError,DecodeError) as exception:
        print(exception)
        return {}

def encode_jwt(user_id)->str:
    return encode({'uid':user_id},secret, algorithm="HS256",headers={
        "alg": "HS256",
        "typ": "JWT"
    })
# Define a route for the root URL
# @app.route('/')
# def hello_world():
#     return 'Nothing'

@app.route('/login', methods=["POST"])
def login():
    print(request.json)
    # If it doesnt satisfy conditions return the code as 400
    body={'username':None,'password':None}
    res= make_response(json.dumps(body), 200)
    print('User attempting to login')
    return res
    

@app.route('/signup', methods=["POST"])
def signup():
    body={'email':None,'username':None,'password':None}
    print(json.dumps(body))
    print(request.json)
    # If it doesnt satisfy conditions return the code as 400
    res= make_response(json.dumps(body), 200)
    print('User attempting to signup')
    
    return res

@app.route('/userinfo')
def getinfo():
    res=make_response()
    res.status_code=204
    print(request.cookies['authToken'])
    # I need to check if I can validate a jwt token from the client side
    authed_token=jwt_auth(request.cookies['authToken'])
    if(authed_token!={}):
  
        res.status_code=200
        #load the user data in the data to this
        res.data= json.dumps({'uid':authed_token['uid']})
        print('here')
        

    return res

# Run the app if this script is executed directly
if __name__ == '__main__':
    app.run(debug=True)