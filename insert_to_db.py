import os
import json
from pymongo import MongoClient

def insert_to_db():
    # Create a MongoDB client
    client = MongoClient('localhost', 27017)

    # Connect to your database
    db = client['video-search-engine']

    # Get the list of JSON files in the data/test directory
    json_files = [file for file in os.listdir('data/test') if file.endswith('.json')]

    for file in json_files:
        # Open each JSON file
        with open(f'data/test/{file}') as f:
            # Load the data from the JSON file
            data = json.load(f)

            # Insert the data into the MongoDB database
            db.test.insert_one(data)

# Call the function
insert_to_db()