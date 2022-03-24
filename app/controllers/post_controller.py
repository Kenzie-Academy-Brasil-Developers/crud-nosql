from http import HTTPStatus
from flask import jsonify, request
from app.models.post_model import Post
from app.exceptions import NotExistentId, KeyInvalid

def read_posts():
    return jsonify(Post.get_all_posts()), HTTPStatus.OK

def read_post_by_id(id: int):
    try:
        return jsonify(Post.get_post_by_id(id)), HTTPStatus.OK
    except NotExistentId:
        return {'error': 'id does not exist in database'}, HTTPStatus.NOT_FOUND
    
def create_post():
    data = request.get_json()
    try:
        post = Post(**data)
        post.create_post()
        return post.__dict__, HTTPStatus.CREATED
    except TypeError:
        return {'error': 'incorrect or missing keys'}, HTTPStatus.BAD_REQUEST
    
def remove_post(id: int):
    try:
        return jsonify(Post.delete_post(id)), HTTPStatus.OK
    except NotExistentId:
        return {'error': 'id does not exist in database'}, HTTPStatus.NOT_FOUND
    
def update_post(id: int):   
    data = request.get_json()
    
    try: 
        expected_key(data)
    except KeyInvalid:
        return {'error': 'incorrect or missing keys'}, HTTPStatus.BAD_REQUEST
    
    try:
        data = Post.updated_date(data)
        update_post = Post.update_post(id, data)
    except NotExistentId:
        return {'error': 'id does not exist in database'}, HTTPStatus.NOT_FOUND

        
    return update_post, HTTPStatus.OK

def expected_key(data: dict):
    expected_key = {"author", "title", "content", "tags"}
    for key in data.keys():
        if not key in expected_key:
            raise KeyInvalid