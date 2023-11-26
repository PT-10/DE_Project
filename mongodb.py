# mongodb.py
import os
import json
import pymongo
from pymongo import MongoClient
import numpy as np
from bson.json_util import dumps
import requests
hf_token = "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"
embedding_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"

class MongoDB:
    def __init__(self):

        # Create a MongoDB client
        self.client = MongoClient('localhost', 27017)

        self.db = self.client['video-search-engine']

    def search(self, query):
        #Implement search logic here
        pass

    def insert_to_db(self):
        # Get the list of JSON files in the data/test directory
        json_files = [file for file in os.listdir('data/test') if file.endswith('.json')]

        for file in json_files:
            # Open each JSON file
            with open(f'data/test/{file}') as f:
                # Load the data from the JSON file
                data = json.load(f)

                # Insert the data into the MongoDB database
                self.db.test.insert_one(data)
                print(f'Inserted {file} to the database')

def generate_embedding(text: str, hf_token: str) -> list[float]:
    response = requests.post(
        embedding_url,
        headers={"Authorization": f"Bearer {hf_token}"},
        json={"inputs": text},
    )

    if response.status_code != 200:
        raise ValueError(
            f"Request failed with status code {response.status_code}: {response.text}"
        )

    return np.array(response.json())

def get_top_k(scores: np.ndarray, k: int) -> np.ndarray:
    idx = np.argpartition(scores, -k)[-k:]
    return idx[np.argsort(scores[idx])][::-1]


def rank(embeddings: list[np.ndarray], query: str, k: int, hf_token: str) -> list[int]:
    if k > len(embeddings):
        raise ValueError("k must be less than the number of videos")

    query_embedding = generate_embedding(query, hf_token)
    embeddings = np.concatenate(embeddings, axis=0)
    dots = np.dot(query, embeddings.T)
    emb_norm = np.linalg.norm(embeddings, axis=1).reshape(1, -1)
    query_norm = np.linalg.norm(query_embedding)
    scores = np.divide(dots, (emb_norm * query_norm)).reshape(-1)
    top_k_idx = get_top_k(scores, k)

    return top_k_idx.tolist()


# for doc in mongo.db.test.find().limit(50):
# 	doc['title_embedding_hf'] = generate_embedding(doc['plot'])
# 	mongo.db.test.replace_one({'_id': doc['_id']}, doc)

# embeddings = []
# # i = 0
# # for video in mongo.db.test.find({}, {"videoInfo.snippet.title": 1}):
# #     title = video.get("videoInfo", {}).get("snippet", {}).get("title", "")
# #     embeddings.append(generate_embedding(title, hf_token))

# # query = "Jawan Hai Mohabbat"
# # print(rank(embeddings, query, 5, hf_token))



# # def embed_all_data(data: list[str], hf_token: str) -> list[np.ndarray]:
# #     embeddings = []
# #     for video in data:
# #         curr_embedding = generate_embedding(video, hf_token)
# #         embeddings.append(curr_embedding)

# #     return embeddings

# mongo = MongoDB()
# client = mongo.client
# db = mongo.db
# def query_with_embedding(client, embedding_query):
#     # # Connect to MongoDB
#     # client = pymongo.MongoClient("your_mongodb_connection_string")
    
#     # # Select the database and collection
#     # db = client["your_database_name"]
#     # test = db["your_test_name"]

#     # Perform aggregation
#     pipeline = [
#         {
#             "$project": {
#                 "_id": 1,
#                 "embedding": 1,  # Replace with the actual field name where your embeddings are stored
#             }
#         },
#         {
#             "$addFields": {
#                 "cosine_similarity": {
#                     "$divide": [
#                         {
#                             "$sum": {
#                                 "$multiply": ["$embedding", embedding_query]
#                             }
#                         },
#                         {
#                             "$sqrt": {
#                                 "$sum": [
#                                     {"$pow": ["$embedding", 2]},
#                                     {"$pow": [embedding_query, 2]}
#                                 ]
#                             }
#                         }
#                     ]
#                 }
#             }
#         },
#         {
#             "$sort": {"cosine_similarity", -1}  # Sort by cosine similarity in descending order
#         }
#     ]

#     result = list(client.test.aggregate(pipeline))

#     # Close the connection
#     client.close()
#     # print(result)
#     return result

# # Example usage
# query = "Jawan Hai Mohabbat"
# query_embedding = generate_embedding(query, hf_token).to
# result = query_with_embedding(client, query_embedding)
# print(result)

