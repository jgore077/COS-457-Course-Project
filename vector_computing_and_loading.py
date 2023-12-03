
from sentence_transformers import SentenceTransformer
from volleyBallDatabase import volleyBallDatabase
import psycopg2
import json

model = SentenceTransformer('all-MiniLM-L6-v2')



# #Our sentences we like to encode
# sentences = ['This framework generates embeddings for each input sentence',
#     'Sentences are passed as a list of string.',
#     'Sentences are passed as a list of string but like a list of strings','sentence generation framework']

# #Sentences are encoded by calling model.encode()
# embeddings = model.encode(sentences)

# # print(cos_sim[embeddings.T[1],embeddings.T[2]])
# embedding_list=embeddings.tolist()
# #Print the embeddings
# # for sentence, embedding in zip(sentences, embeddings):
# #     embedding_list.append(embedding)
# #     print(type(embedding.tolist()))
# print(cos_sim(embedding_list[1],embedding_list[2]))
# print(cos_sim(embedding_list[0],embedding_list[2]))
# print(cos_sim(embedding_list[0],embedding_list[3]))

with open('config.json','r') as data:
    config=json.load(data)

connection = psycopg2.connect(**config)

cursor =connection.cursor()
db = volleyBallDatabase(cursor=cursor,connection=connection)

for announcement in db.fetch_announcements():
    encoded_announcement=json.dumps({"description":model.encode(announcement[3]).tolist()})
    db.insert_vectorized_entry(announcement[0],'announcements',encoded_announcement)
    
for game in db.fetch_games():
    encoded_game=json.dumps({'description':model.encode(game[1]).tolist(),
                             'location':model.encode(game[2]).tolist(),
                             'opponent':model.encode(game[4]).tolist()})
    db.insert_vectorized_entry(game[0],'games',encoded_game)
    
for practice in db.fetch_practice():
     encoded_practice=json.dumps({'description':model.encode(practice[1]).tolist(),
                             'location':model.encode(practice[2]).tolist()})
     db.insert_vectorized_entry(practice[0],'practice',encoded_practice)

    