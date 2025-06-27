# Save this as app.py

from flask import Flask, jsonify, request
from flask_cors import CORS
from trie_copy import Trie
import json

app = Flask(__name__)
CORS(app)
trie = Trie()

with open("movies.json", "r") as file:
    data = json.load(file)

counter = 1
for d in data:
    trie.insert(d["title"], d["url"])
    print(counter, d["title"])
    counter += 1

@app.route('/api/search', methods=['GET'])
def hello():
    query = request.args.get('query')

    movies = trie.search(query)
    return jsonify({
        'movies': movies
    })

if __name__ == '__main__':
    app.run(debug=True, port=3000)
