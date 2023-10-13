# post_service.py

from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# URL_REQ = "http://127.0.0.1:5000/user/"
URL_REQ = "https://userservicecontainer.wonderfulocean-aa423ae1.canadacentral.azurecontainerapps.io/user/"

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
    # posts = {
    #     '1': {'user_id': '1', 'post': 'Hello, world!'},
    #     '2': {'user_id': '2', 'post': 'My first blog post'}
    # }
    # post_info = posts.get(id, {})
    post_info = None
    for post in posts:
        if int(post['id']) == int(id):
            post_info = post
            break
    
    # Get user info from User Service
    if post_info:
        response = requests.get(f'{URL_REQ}{post_info["user_id"]}')
        if response.status_code == 200:
            post_info['user'] = response.json()

    return jsonify(response.json())

# -C- Create post
@app.route('/post', methods=['POST'])
def create_post():
    user_REQ = requests.get(f'{URL_REQ}{request.json["user_id"]}')
    
    # new_post['user'] = user_REQ
    new_post = {
    'id': request.json['id'],
    'user_id': request.json['user_id'],
    'post': request.json['post'],
    'user': user_REQ.json()
    }
    posts.append(new_post)
    return jsonify({'Success': new_post})

# -U- update post 
@app.route('/post/<id>', methods=['PUT'])
def update_post(id):
    a_post = None

    for post in posts:
        if int(post['id']) == int(id):
            a_post = post
            break

    if a_post == None:
        return jsonify({'error:': 'post not found'})
    
    a_post['user_id'] = request.json['user_id']
    a_post['post'] = request.json['post']

    return jsonify({'updated': a_post})

# -D- DELETE post
@app.route('/post/<id>', methods=['DELETE'])
def delete_post(id):
    a_post = None
    for post in posts:
        if int(post['id']) == int(id):
            a_post = post
            break

    if a_post == None:
        return jsonify({'error:': 'user not found'})
    
    posts.remove(a_post)
    return jsonify("Deleted successfully")

if __name__ == '__main__':
    app.run(port=5001)