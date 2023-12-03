
#This will be used for communicating with the database then with the web app
from flask import Flask,make_response,request,jsonify
# psycopg2 is a library for connecting
import psycopg2
import json
from jwt import InvalidSignatureError,DecodeError,decode,encode
import re
from datetime import datetime
from volleyBallDatabase import volleyBallDatabase
from numpy import dot
from numpy.linalg import norm
from sentence_transformers import SentenceTransformer
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

model = SentenceTransformer('all-MiniLM-L6-v2')


vectorized_data=db.fetch_vectorized_tables()

vector_table_dict=dict()
for entry in vectorized_data:
    if entry[1] not in vector_table_dict.keys():
        vector_table_dict[entry[1]]= [entry]
        continue
    vector_table_dict[entry[1]].append(entry)

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
    return make_response(json.dumps({'players':users_and_emails_list}),200)
# Run the app if this script is executed directly

@app.route('/games')
def games():
    games_list=[]
    games =db.fetch_games()

    for row in games:
        games_list.append({'game_id':row[0],'location':row[1],'description':row[2],'gamedate':row[3].strftime("%Y-%m-%d %H:%M:%S"),'opponent':row[4],'game_score':row[5]})
    return make_response(json.dumps({'games':games_list}),200)

output_format = "%Y-%m-%d %H:%M:%S"

@app.route('/announcements')
def announcements():
    announcements_list=[]
    announcements =db.fetch_announcements()

    for row in announcements:
         announcements_list.append({'id':row[0],'description':row[3],'datetime':row[2].strftime("%Y-%m-%d %H:%M:%S")})
    return make_response(json.dumps({'announcements':announcements_list}),200)

@app.route('/practices')
def practices():
    practice_list=[]
    practices =db.fetch_practice()

    for row in practices:
         practice_list.append({'id':row[0],'description':row[1],'location':row[2],'datetime':row[3].strftime("%Y-%m-%d %H:%M:%S")})
    return make_response(json.dumps({'practices':practice_list}),200)

@app.route('/creategame',methods=["POST"])
def creategame():
    
    db.insert_game(request.json['location'],request.json['description'],datetime.strptime(request.json['datetime'], "%Y-%m-%dT%H:%M:%S.%fZ").strftime(output_format),request.json['opponent'])
    return make_response({},200)

@app.route('/createpractice',methods=["POST"])
def createpractice():
   return make_response({},200)

@app.route('/createannouncement',methods=["POST"])
def createannouncement():
   db.insert_announcement(request.json['user_id'],datetime.strptime(request.json['datetime'], "%Y-%m-%dT%H:%M:%S.%fZ").strftime(output_format),request.json['description'])
   return make_response({},200)

@app.route('/updategame',methods=["POST"])
def updategame():
   
    db.update_game(request.json['id'],request.json['location'],request.json['opponent'],datetime.strptime(request.json['datetime'], "%Y-%m-%dT%H:%M:%S.%fZ").strftime(output_format),request.json['datetime'])
    return make_response({},200)

@app.route('/updatepractice',methods=["POST"])
def updatepractice():
    return make_response({},200)

@app.route('/updateannouncement',methods=["POST"])
def updateannouncement():
   print(request.json['id'],request.json['description'])
   db.update_announcement(request.json['id'],request.json['description'])
   return make_response({},200)

@app.route('/userinfo',methods=["POST"])
def userinfo():
    try:
        authCookie=request.json['authCookie']
    except Exception as e:
        print(e)
        return make_response({},500)

    decodedAuthToken= jwt_auth(authCookie)
    
    if(decodedAuthToken=={}):
        return make_response({},500)
    print(decodedAuthToken)
    user_info=db.fetch_all_user(decodedAuthToken['uid'])[0]
    print(user_info)
    return make_response(json.dumps({'username':user_info[2],'number':user_info[5],'commuter':user_info[6],'shirt':user_info[7]}),200)

@app.route('/shirt',methods=["POST"])
def shirt():
    shirt_size=request.json['shirt']
    try:
        authCookie=request.json['authCookie']
    except Exception as e:
        print(e)
        return make_response({},500)

    decodedAuthToken= jwt_auth(authCookie)
    
    if(decodedAuthToken=={}):
        return make_response({},500)
    
    db.update_user_shirt_size(decodedAuthToken['uid'],shirt_size)
    return make_response({},200)

@app.route('/phone',methods=["POST"])
def phone():
    phone_number=request.json['phone']
    try:
        authCookie=request.json['authCookie']
    except Exception as e:
        print(e)
        return make_response({},500)

    decodedAuthToken= jwt_auth(authCookie)
    
    if(decodedAuthToken=={}):
        return make_response({},500)
    
    db.update_user_phone_number(decodedAuthToken['uid'],phone_number)
    return make_response({},200)

@app.route('/commuter',methods=["POST"])
def commuter():
    commuter_status=request.json['commuter']
    try:
        authCookie=request.json['authCookie']
    except Exception as e:
        print(e)
        return make_response({},500)

    decodedAuthToken= jwt_auth(authCookie)
    
    if(decodedAuthToken=={}):
        return make_response({},500)
    
    db.update_user_commuter_status(decodedAuthToken['uid'],commuter_status)
    return make_response({},200)
 
 # Match search functionality
@app.route('/search_matches', methods=['GET'])
def search_matches():
    date = request.args.get('date')
    location = request.args.get('location')

    matches = db.search_matches(date, location)
    matches_list = [{'date': match[0].strftime("%Y-%m-%d"), 'location': match[1]} for match in matches]
    
    return jsonify(matches_list)

#News Search 
@app.route('/search_news', methods=['GET'])
def search_news():
    date_published = request.args.get('date_published')
    content = request.args.get('content')

    news_items = db.search_news(date_published, content)
    news_list = [{'id': item[0], 'publisher_uid': item[1], 'date_published': item[2].strftime("%Y-%m-%d"), 'content': item[3]} for item in news_items]
    
    return jsonify(news_list)


def cos_sim(a,b):
    return dot(a, b)/(norm(a)*norm(b))

@app.route('/search',methods=["POST"])
def search():
    
    query=request.json['query']
    method=request.json['method']
    attribute=request.json['attribute']
    table=request.json['table']
    try:
        datetime=request.json['datetime']
    except KeyError:
        datetime=None
    results={}
    if method=='Broad Search':
        db_results=db.broad_search(query)
        results={'announcements':db_results[0],'games':db_results[2],'practices':db_results[3],'players':db_results[4]}
    elif method=='Precision Search':
        pass    
    elif method=='Match Search':
        print(datetime)
        results['games']=db.search_matches(location=query,date=datetime)
    elif method=='News Search':
        #                       db.search_news(content=query,date_published=None)
        results['announcements']=db.search_news(content=query,date_published=datetime)
    elif method=='Vector Search':
        encoded_query=model.encode(query).tolist()
        
        announcement_list=list()
        practice_list=list()
        games_list=list()
        
        for announcement in vector_table_dict['announcements']:
            if cos_sim(announcement[2]['description'],encoded_query)>.5:
                announcement_list.append(announcement[0])
                
        for game in vector_table_dict['games']:
              if cos_sim(game[2]['opponent'],encoded_query)>.5 or cos_sim(game[2]['description'],encoded_query)>.5 or cos_sim(game[2]['location'],encoded_query)>.5:
                games_list.append(game[0])
                
        for practice in vector_table_dict['practice']:
            if cos_sim(practice[2]['description'],encoded_query)>.5 or cos_sim(practice[2]['location'],encoded_query)>.5:
                practice_list.append(practice[0])
    
        game_entrys=db.fetch_all_entrys_from_ids('games',games_list)
        announcement_entrys=db.fetch_all_entrys_from_ids('announcements',announcement_list)
        practice_entrys=db.fetch_all_entrys_from_ids('practice',practice_list)
        
        results['games']=[{'game_id': row[0],'location': row[1],'description': row[2],'gamedate': row[3].strftime("%Y-%m-%d %H:%M:%S"),'opponent': row[4],'game_score': row[5]}for row in game_entrys]#{'game_id':row[0],'location':row[1],'description':row[2],'gamedate':row[3].strftime("%Y-%m-%d %H:%M:%S"),'opponent':row[4],'game_score':row[5]}
        results['announcements']=[{'id':row[0],'description':row[3],'datetime':row[2].strftime("%Y-%m-%d %H:%M:%S")}for row in announcement_entrys]
        results['practices']=[{'id':row[0],'description':row[1],'location':row[2],'datetime':row[3].strftime("%Y-%m-%d %H:%M:%S")} for row in practice_entrys]
        
    for key in results.keys():
        if results[key]==[]:
            results[key]=None
    print(request.json)
    return make_response(json.dumps(results),200)
    

if __name__ == '__main__':   
    app.run(debug=True)
 