from flask import Flask, render_template
from mongodb import MongoDB, generate_embedding
#from setup import DatabaseSetup
import numpy as np
from flask import jsonify, request,redirect,session
from mysql import verify_user,create_user, clicked

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


@app.route('/video/<video_id>')
def video_page(video_id):
    # Fetch video details based on the video_id
    # This is where you would retrieve information about the selected video
    # For example, you might fetch details from a database or an API
    video_details = get_video_details(video_id)

    # Render the video page template with the video details
    return render_template('video_details.html', video_details=video_details)

def get_video_details(video_id):
    video_details = db.test.find_one({ "videoInfo.id": video_id })
    return video_details

if __name__=="__main__":
    app.run(debug=True)
