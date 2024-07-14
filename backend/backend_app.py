from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json()
    if not data or not 'title' in data or not 'content' in data:
        return jsonify({'error': 'Both title and content are required'}), 400

    new_id = max(post['id'] for post in POSTS) + 1 if POSTS else 1
    new_post = {
        'id': new_id,
        'title': data['title'],
        'content': data['content']
    }
    POSTS.append(new_post)
    return jsonify(new_post), 201


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
