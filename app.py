from flask import Flask, render_template
from mongodb import MongoDB, generate_embedding
from setup import DatabaseSetup
import numpy as np
from flask import jsonify, request

hf_token = "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"
embedding_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"

app = Flask(__name__)

mongo = MongoDB()
# mongo.insert_to_db()
# counter=0
# counter_done=0
# for video in mongo.db.test.find():
#     if counter > 50:
#         break
#     if video.get('title_embedding_hf'):
#         counter_done+=1
#         continue
#     title = video.get("videoInfo", {}).get("snippet", {}).get("title", "")
#     print(title)
#     video['title_embedding_hf'] = generate_embedding(title, hf_token).tolist()
#     mongo.db.test.replace_one({'_id': video['_id']}, video)
#     counter+=1
# print(counter_done)
# for video in mongo.db.test.find({}, {"videoInfo.snippet.title": 1}):
#     title = video.get("videoInfo", {}).get("snippet", {}).get("title", "")
#     embeddings.append(generate_embedding(title, hf_token))
# query ="Jawans"
# q_embedding = generate_embedding(query, hf_token)

# def get_top_k(scores: np.ndarray, k: int) -> np.ndarray:
#     idx = np.argpartition(scores, -k)[-k:]
#     return idx[np.argsort(scores[idx])][::-1]


# def rank(embeddings: list[np.ndarray], query: str, k: int, hf_token: str) -> list[int]:
#     if k > len(embeddings):
#         raise ValueError("k must be less than the number of videos")

#     query_embedding = generate_embedding(query, hf_token)
#     embeddings = np.concatenate(embeddings, axis=0)
#     dots = np.dot(query, embeddings.T)
#     emb_norm = np.linalg.norm(embeddings, axis=1).reshape(1, -1)
#     query_norm = np.linalg.norm(query)
#     scores = np.divide(dots, (emb_norm * query_norm)).reshape(-1)
#     top_k_idx = get_top_k(scores, k)

#     return top_k_idx.tolist()



@app.route('/')
def index():
    return render_template("index.html")

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get('query')
      # Replace with your actual Hugging Face token

    if not query:
        return jsonify({"error": "Query parameter 'query' is required"}), 400

    embeddings = mongo.embed_all_data(hf_token)
    result_indices = mongo.rank(embeddings, query, k=5, hf_token=hf_token)

    # Retrieve the details of the top 5 videos based on the search
    top_videos = [mongo.db.test.find_one({'_id': embeddings_index}) for embeddings_index in result_indices]

    # Return the results as JSON
    print(jsonify({"results": top_videos}))


@app.route("/video/<video_id>")
def video_details(video_id):
    # Fetch video details from MongoDB and Neo4j
    # Update CVP and SRP accordingly
    return render_template("video_details.html")

if __name__=="__main__":
    app.run(debug=True)