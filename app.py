# Save this as app.py

from flask import Flask, jsonify, request
from flask_cors import CORS
from trie import Trie
import json
from time import time

app = Flask(__name__)
CORS(app)

trie = Trie()

RATE_LIMIT = 10       # Máximo requests
TIME_WINDOW = 60      # En segundos

requests_log = {}

def cleanup_old_requests(ip, now):
    window_start = now - TIME_WINDOW
    requests_log[ip] = [t for t in requests_log.get(ip, []) if t > window_start]

@app.before_request
def rate_limit():
    ip = request.remote_addr
    now = time()
    cleanup_old_requests(ip, now)

    if len(requests_log.get(ip, [])) >= RATE_LIMIT:
        return jsonify({"error": "Too many requests"}), 429

    requests_log.setdefault(ip, []).append(now)

with open("movies.json", "r") as file:
    data = json.load(file)

for d in data:
    trie.insert(d["title"], d["url"])

@app.route('/api/search', methods=['GET'])
def hello():
    query = request.args.get('query')

    movies = trie.search(query)
    return jsonify({
        'movies': movies
    })

if __name__ == '__main__':
    app.run(debug=True, port=3000)
