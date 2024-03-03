# DE_Project

1. Create a virtual environment:
```bash
python -m venv de_env
```
2. Activate the virtual environment (PowerShell):
```bash
cd /path/to/new/virtual/environment
```
```bash
de_env/Scripts/Activate.ps1
```
3. Navigate to the root directory of your project and set flask app:
```bash
cd /path/to/root/directory
```
```bash
set FLASK_APP=app.py
```
4. Before running flask app, ensure mongodb is running:
```bash
cd C:\Program Files\MongoDB\Server\7.0\bin
```
```bash
mongod --dbpath C:\Users\<user>\projects\DE_Project\data\test
```
5. Run flask app:
```bash
python -m flask run
```

