import jwt
with open('private.key','r') as data:
    secret=data.read()

encoded_jwt = jwt.encode({"uid": 0}, secret, algorithm="HS256",headers={
  "alg": "HS256",
  "typ": "JWT"
})
print(encoded_jwt)

print(jwt.decode(encoded_jwt, secret, algorithms=["HS256"]))