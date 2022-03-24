import pymongo
from pymongo import ReturnDocument
from datetime import datetime as dt

from app.exceptions import NotExistentId

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['kenzie']

class Post:
    def __init__(self,title, author, tags, content):
        self.title = title
        self.author = author
        self.tags = tags
        self.content = content
    
    @staticmethod
    def get_all_posts():
        return list(db.posts.find())
    
    @staticmethod
    def get_post_by_id(id: int):
        post = list(db.posts.find({'_id': id}))
        
        if len(post) == 0:
            raise NotExistentId
        
        return post
    
    @staticmethod
    def update_post(id: int, payload: dict):
        post = db.posts.find_one_and_update({"_id": id}, {"$set": payload}, return_document=ReturnDocument.AFTER)

        if not post:
            raise NotExistentId
        
        return post
    
    @staticmethod
    def delete_post(id: int):
        post = db.posts.find_one_and_delete({'_id': id})
        
        if not post:
            raise NotExistentId
        
        return post
    
    @staticmethod    
    def updated_date(data: dict):
        data['update_at'] = dt.now().strftime("%d/%m/%Y %H:%M:%S")
        return data
    
    def creation_date(self):
        self.created_at = dt.now().strftime("%d/%m/%Y %H:%M:%S")
        
    def add_id(self):
        posts_list = list(self.get_all_posts())
        
        if len(posts_list) == 0:
            self._id = 1
        else:
            self._id = posts_list[-1]['_id'] + 1
    
    def create_post(self):
        self.add_id()
        self.creation_date()
        
        db.posts.insert_one(self.__dict__)