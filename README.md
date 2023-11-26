# DE_Project

python -m venv de_env

cd /path/to/new/virtual/environment
de_env/Scripts/Activate.ps1 (powershell)

cd to root directory
set FLASK_APP=app.py
python -m flask run

before starting the flask server
run mongodb server -> cd C:\Program Files\MongoDB\Server\7.0\bin
run the command -> mongod
mongod --dbpath C:\Users\prash\projects\DE_Project\data\test