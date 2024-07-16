from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from datetime import date
from storage import *

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = read_data('posts.json')  # Use the updated file path


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """Returns a JSON file containing the list of blog posts. Optionally, it
     can sort the list of posts according to the specified attribute and
      direction."""
    sort = request.args.get('sort')
    direction = request.args.get('direction')

    if not sort and not direction:
        return jsonify(POSTS), 200

    if sort not in ['title', 'content', 'author', 'post_date'] or direction not in ['asc', 'desc']:
        return jsonify({'error': 'To sort please select: title / content /'
                                 ' author / post_date and direction: asc or desc'}), 400

    if sort == 'title':
        if direction == 'asc':
            sorted_posts = sorted(POSTS, key=lambda x: x['title'])
        elif direction == 'desc':
            sorted_posts = sorted(POSTS, key=lambda x: x['title'], reverse=True)
    elif sort == 'content':
        if direction == 'asc':
            sorted_posts = sorted(POSTS, key=lambda x: x['content'])
        elif direction == 'desc':
            sorted_posts = sorted(POSTS, key=lambda x: x['content'], reverse=True)
    elif sort == 'author':
        if direction == 'asc':
            sorted_posts = sorted(POSTS, key=lambda x: x['author'])
        elif direction == 'desc':
            sorted_posts = sorted(POSTS, key=lambda x: x['author'], reverse=True)
    elif sort == 'post_date':
        if direction == 'asc':
            sorted_posts = sorted(POSTS, key=lambda x: x['post_date'])
        elif direction == 'desc':
            sorted_posts = sorted(POSTS, key=lambda x: x['post_date'], reverse=True)

    return jsonify(sorted_posts), 200


@app.route('/api/posts', methods=['POST'])
def add_post():
    """Creates a new blog entry. Expects both title and content. If these are
     specified, the new post will be returned or an error if the input is
      invalid."""
    data = request.get_json()
    if not data or not 'title' in data or not 'content' in data:
        return jsonify({'error': 'Both title and content are required'}), 400

    new_id = max(post['id'] for post in POSTS) + 1 if POSTS else 1
    new_post = {
        'id': new_id,
        'title': data['title'],
        'content': data['content'],
        'author': data.get('author', 'Anonymous'),
        'post_date': date.today().strftime('%Y-%m-%d')
    }
    POSTS.append(new_post)
    sync_data('posts.json', POSTS)
    return jsonify(new_post), 201


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    """Deletes a post based on the ID specified in the URL. If the post
     exists, it is deleted, if it does not exist, an error message is
      returned."""
    for post in POSTS:
        if post['id'] == id:
            POSTS.remove(post)
            return jsonify({"message": f"Post with id {id} has been deleted"
                                       f" successfully."}), 200
    sync_data('posts.json', POSTS)
    return jsonify({"message": f"Post with id {id} not found."}), 404


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update(id):
    """Updates an existing blog post with a new title or content."""
    data = request.get_json()
    for post in POSTS:
        if post['id'] == id:
            title = data.get('title', post['title'])
            content = data.get('content', post['content'])
            author = data.get('author', post['author'])
            post_date = date.today().strftime('%Y-%m-%d')
            updated_post = {
                'id': id,
                'title': title,
                'content': content,
                'author': author,
                'post_date': post_date
            }
            post.update(updated_post)
            update_post_in_json('posts.json', updated_post)
            return jsonify({"message": f"Post with id {id} has been updated "
                                       f"successfully."}), 200
    return jsonify({"message": f"Post with id {id} not found."}), 404


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """Searches for posts based on their title or content. Displays an error
     message if no search parameters are specified or if no matches are found."""
    title = request.args.get('title')
    content = request.args.get('content')
    author = request.args.get('author')
    post_date = request.args.get('post_date')

    if not title and not content and not author and not post_date:
        return jsonify({"message": "Please provide a title/content/author/date to search."}), 400

    filtered_posts = []
    for post in POSTS:
        if ((title and title.lower() in post['title'].lower()) or
                (content and content.lower() in post['content'].lower())
                or (author and author.lower() in post['author'].lower())
                or (post_date and post_date == post['post_date'])):
            filtered_posts.append(post)
        if filtered_posts:
            return jsonify(filtered_posts), 200

    error_message_parts = []
    if title:
        error_message_parts.append(f"title: '{title}'")
    if content:
        error_message_parts.append(f"content: '{content}'")
    if author:
        error_message_parts.append(f"author: '{author}'")
    if post_date:
        error_message_parts.append(f"date: '{post_date}'")
    error_message = " or ".join(error_message_parts)

    return jsonify({"message": f"No posts found with the {error_message}"}), 404


SWAGGER_URL = "/api/docs"  # (1) swagger endpoint e.g. HTTP://localhost:5002/api/docs
API_URL = "/static/blog.json"  # (2) ensure you create this dir and file

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Blog API'  # (3) You can change this if you like
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
