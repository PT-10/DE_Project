from flask import Flask, render_template
from mongodb import MongoDB, generate_embedding
#from setup import DatabaseSetup
import numpy as np
from flask import jsonify, request,redirect,session
from mysql import verify_user,create_user

hf_token = "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"
embedding_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"



app = Flask(__name__)
app.secret_key = 'any random string'
mongo = MongoDB()
db = mongo.db
def search_videos(query):
    # Create a text index on the fields you want to search
    db.test.create_index([("videoInfo.snippet.title", "text"), ("videoInfo.snippet.tags", "text")])

    # Use the $text operator for text search
    result = db.test.find(
        {"$text": {"$search": query}},
        {"score": {"$meta": "textScore"}}
    ).sort([("score", {"$meta": "textScore"})]).limit(7)

    return list(result)

def extract_titles(results):
    # Extract titles from the search results
    titles = [result["videoInfo"]["snippet"]["title"] for result in results]
    return titles
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
def default():
    return render_template("login.html")

@app.route('/login', methods = ['POST', 'GET'])
def login():
    user = ""
    trending = []
    subscriptions = []
    recommended = []
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        valid = verify_user(username,password)
        if valid != 1:
             return redirect("/")
        else:
            session['username'] = username
            return render_template('index.html')
    else:
        return render_template('login.html', result = [])

@app.route('/register', methods = ['POST', 'GET'])
def register():
	# print "in register"
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		valid = create_user(username,password)
		if valid == 0 or valid == 5:
			return render_template('/index1.html',result = [False, "", recent(),[],[],True])
		if valid == 10:
			session['username'] = username
		return redirect("/")

@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        search_query = request.form['search_query']

        # Call your MongoDB search function
        results = search_videos(search_query)

        # Pass the results to the template
        return render_template('search_results.html', search_results=results)


@app.route("/video/<video_id>")
def video_details(video_id):
    # Fetch video details from MongoDB and Neo4j
    # Update CVP and SRP accordingly
    return render_template("video_details.html")

if __name__=="__main__":
    app.run(debug=True)


# from flask import Flask, render_template, redirect, url_for, request
# from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'your_secret_key'

# login_manager = LoginManager(app)

# class User(UserMixin):
#     def __init__(self, user_id):
#         self.id = user_id

# @login_manager.user_loader
# def load_user(user_id):
#     return User(user_id)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         # Replace this with your actual authentication logic
#         username = request.form['username']
#         password = request.form['password']

#         # Example authentication (replace with your own logic)
#         if username == 'your_username' and password == 'your_password':
#             user = User(user_id=1)
#             login_user(user)
#             return redirect(url_for('index'))

#         # Redirect to login page with an error message on failed login
#         return render_template('login.html', error='Invalid username or password')

#     return render_template('login.html')

# @app.route('/logout')
# def logout():
#     logout_user()
#     return 'Logged out successfully'

# @app.route('/index')
# def index():
#     return render_template('index.html')

# if __name__ == '__main__':
#     app.run(debug=True)
