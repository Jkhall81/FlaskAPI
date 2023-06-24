from flask import Flask, jsonify, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

posts = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
    {"id": 3, "title": "Third post", "content": "This is the third post."},

]


def find_post_by_id(post_id):
    """ searches list of dictionaries to see if passed in post_id is present.
    If post_id is present that post is returned, if not None gets returned!"""
    for post in posts:
        if post['id'] == post_id:
            return post
    return None


def validate_post_data(data):
    """ Checks to see if POST request body contains a title and content."""
    if 'title' not in data or 'content' not in data:
        return False
    return True


@app.errorhandler(404)
def not_found_error(error):
    """ 404 error handling."""
    return jsonify({'error': 'Not Found'}), 404


@app.errorhandler(405)
def method_not_allowed_error(error):
    """ 405 error handling."""
    return jsonify({'error': 'Method Not Allowed'}), 405


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    title = request.args.get('title')
    content = request.args.get('content')

    if title:
        for index, post in enumerate(posts):
            if title in post['title']:
                return posts[index], 200

    if content:
        for index, post in enumerate(posts):
            if content in post['content']:
                return posts[index], 200

    return jsonify({'message': 'No posts with matching parameters found!'}), 400


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    post = find_post_by_id(id)
    if post is None:
        return 'Post not found homie!', 404
    target_index = 0
    for index, post in enumerate(posts):
        if id == post['id']:
            target_index = index

    else:
        new_post = request.get_json()
        if 'content' not in new_post and 'title' not in new_post:
            return jsonify({'message': 'Invalid PUT data!'}), 400
        elif 'title' not in new_post:
            posts[target_index]['content'] = new_post['content']
        elif 'content' not in new_post:
            posts[target_index]['title'] = new_post['title']
        else:
            posts[target_index]['content'] = new_post['content']
            posts[target_index]['title'] = new_post['title']

    return posts[target_index], 200


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    post = find_post_by_id(id)

    if post is None:
        return 'Post not found homie!', 404
    else:
        for index, post in enumerate(posts):
            if post['id'] == id:
                del posts[index]
    return jsonify({'message': f'Post with id {id} has been deleted successfully!'}), 200


@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
    """ This function returns JSON data of posts list if its a GET request and
    if it's a valid POST request it repeats the users input.  It returns an error message
    if the POST request is not valid."""
    if request.method == 'POST':
        new_post = request.get_json()

        # This shit is saying if validate_post_data returns False as fuck then...
        if not validate_post_data(new_post):
            return jsonify({'error': 'Invalid post data'}), 400

        new_id = max(post['id'] for post in posts) + 1
        new_post['id'] = new_id

        posts.append(new_post)

        return jsonify(new_post), 20

    sort = request.args.get('sort')
    direction = request.args.get('direction')
    if sort:
        reverse = None
        if direction == 'asc':
            reverse = False
        elif direction == 'desc':
            reverse = True
        else:
            return jsonify({'error': 'Invalid direction parameter!'}), 400

        if reverse is not None:
            if sort not in ('title', 'content') or direction not in ('asc', 'desc'):
                return jsonify({'error': 'Invalid parameters used!'}), 400

            if sort == 'title':
                sorted_by_title = sorted(posts, key=lambda x: x['title'], reverse=reverse)
                return sorted_by_title
            elif sort == 'content':
                sorted_by_content = sorted(posts, key=lambda x: x['content'], reverse=reverse)
                return sorted_by_content

    return jsonify(posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
