# post_service.py

from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

posts = [
    {'id': 1, 'user_id': 1, 'post': 'Hello, world!'},
    {'id': 2, 'user_id': 2, 'post': 'My first blog post'}   
]

@app.route('/')
def home():
    return jsonify(posts)
    return "Hello from Post Service!"


# -R- Read post by id
@app.route('/post/<id>')
def post(id):
    posts = {
        '1': {'user_id': '1', 'post': 'Hello, world!'},
        '2': {'user_id': '2', 'post': 'My first blog post'}
    }
    post_info = posts.get(id, {})
    
    # Get user info from User Service
    if post_info:
        response = requests.get(f'http://127.0.0.1:5000/user/{post_info["user_id"]}')
        if response.status_code == 200:
            post_info['user'] = response.json()

    return jsonify(post_info)

# -C- Create post
@app.route('/post', methods=['POST'])
def create_post():
    new_post = {
        'id': request.json['id'],
        'user_id': request.json['user_id'],
        'post': request.json['post']
    }
    posts.append(new_post)
    return jsonify({'Success': new_post})

if __name__ == '__main__':
    app.run(port=5001)