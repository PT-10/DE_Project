from flask import Flask, render_template
from mongodb import MongoDB, generate_embedding
#from setup import DatabaseSetup
import numpy as np
from flask import jsonify, request,redirect,session
from mysql import verify_user,create_user
# from insert_to_neo import insert_to_neo,add_video_relations

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
    print(list(result))

    return list(result)

def extract_titles(results):
    # Extract titles from the search results
    titles = [result["videoInfo"]["snippet"]["title"] for result in results]
    return titles
 
def get_top_k(scores: np.ndarray, k: int) -> np.ndarray:
    idx = np.argpartition(scores, -k)[-k:]
    return idx[np.argsort(scores[idx])][::-1]


def rank(embeddings, query: str, k: int, hf_token: str) -> list[str]:
    if k > len(embeddings):
        raise ValueError("k must be less than the number of videos")
    video_ids = [curr_dict["_id"] for curr_dict in embeddings]

    # Separate the embeddings and video IDs
    video_ids, embeddings = zip(*[(video['_id'], video['title_embedding_hf']) for video in embeddings])

    print(embeddings[0])
    print(np.array(embeddings[0]).shape)

    embeddings = [np.array(i).reshape(1, -1) for i in embeddings]

    query_embedding = generate_embedding(query, hf_token)
    embeddings = np.concatenate(embeddings, axis=0)
    print(embeddings.shape)
    dots = np.dot(query_embedding, embeddings.T)
    emb_norm = np.linalg.norm(embeddings, axis=1).reshape(1, -1)
    query_norm = np.linalg.norm(query_embedding)
    scores = np.divide(dots, (emb_norm * query_norm)).reshape(-1)
    top_k_idx = get_top_k(scores, k)
    list_ix=[video_ids[i] for i in top_k_idx]
    query = {"_id": {"$in": list_ix}}
    # Return the top k video IDs instead of the indices
    return list(db.test.find(query))


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
            # insert_to_neo()
            # add_video_relations()
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
			return render_template('/index1.html')
		if valid == 10:
			session['username'] = username
		return redirect("/")

@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        search_query = request.form['search_query']

        # Call your MongoDB search function
        embeddings=list(db.test.find({}, {"title_embedding_hf": 1,"_id":1}))
        # print(embeddings) 
        results = rank(embeddings,search_query, 7, hf_token)
        # results = search_videos(search_query)


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
