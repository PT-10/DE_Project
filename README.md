# DE_Project

1. Create a virtual environment:
   ```
   python -m venv de_env
   ```
2. Activate the virtual environment (PowerShell):
```
cd /path/to/new/virtual/environment
de_env/Scripts/Activate.ps1
```
3. Navigate to the root directory of your project and set flask app:
   ```
   cd /path/to/root/directory
   set FLASK_APP=app.py
   ```
4. Before running flask app, ensure mongodb is running:
   ```
   cd C:\Program Files\MongoDB\Server\7.0\bin
    mongod --dbpath C:\Users\<user>\projects\DE_Project\data\test
   ```
5. Run flask app:
   ```
   python -m flask run

   ```
