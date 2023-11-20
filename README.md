# COS-457-Course-Project


**Technologys Utilized**
<p float="left">
  <img src="https://cdn-icons-png.flaticon.com/512/5968/5968342.png" width="100" />
  <img src="https://cdn-icons-png.flaticon.com/512/5968/5968322.png" width="100" /> 
  <img src="https://cdn-icons-png.flaticon.com/512/5968/5968350.png" width="100" />
  <img src="https://upload.wikimedia.org/wikipedia/commons/a/a7/React-icon.svg" width="100" />
</p>

**Installation**

Firstly install python modules
```
pip install -r requirements.txt
```
Secondly navigate to "vbms-frontend" directory
```
cd ./vbms-frontend
```
Then install all node modules
```
npm i
```
<hr/>

**Running**

Windows 
```
./run.ps1
```
Linux
```
./run.sh
```
**Technical Details**

The backend uses ```flask``` to create an api which interacts with database with a postGres connector called ```psycopg2```.
The backend also has a class called volleyBallData which contains many of the methods neccesary to interact with the database.

The frontend is made with _React_ and will send requests to the backend to serve data to users. 

The interface also allows users to interface with the database at a level determined by their role on the team. For example every user can change 
their shirt size, phone number and commuter status but not all users can edit/create games.