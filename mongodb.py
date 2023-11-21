# mongodb.py
from pymongo import MongoClient

class MongoDB:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['video_search_engine']

    def search(self, query):
        results = self.db.videos.find({"$text": {"$search": query}})
        return [result for result in results]