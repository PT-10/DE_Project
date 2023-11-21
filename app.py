from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    # Handle the search query here
    # Perform search in MongoDB and fetch relevant videos
    # Update SRP and CVP accordingly
    return render_template("search_results.html")

@app.route("/video/<video_id>")
def video_details(video_id):
    # Fetch video details from MongoDB and Neo4j
    # Update CVP and SRP accordingly
    return render_template("video_details.html")

if __name__=="__main__":
    app.run(debug=True)