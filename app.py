# app.py
from flask import Flask, request, jsonify
from mongodb import MongoDB

app = Flask(__name__)
db = MongoDB()

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    results = db.search(query)
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)