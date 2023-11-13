import jwt
with open('private.key','r') as data:
    secret=data.read()

encoded_jwt = jwt.encode({"uid": 0}, secret, algorithm="HS256",headers={
  "alg": "HS256",
  "typ": "JWT"
})
encoded_jwt='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjEsInJvbGUiOiJhZG1pbiJ9.Z2W4RWCIYYhFgYvKefm_k7K1SglpP-koKtWcbvnrmuY'

print(jwt.decode(encoded_jwt, secret, algorithms=["HS256"]))