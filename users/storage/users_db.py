from bson.objectid import ObjectId
from pymongo import MongoClient

from entities import User
from utils import INTERNAL_ERROR, UsersError


HOST = 'localhost'
PORT = 27017


class UsersDB(object):
    def __init__(self):
        client = MongoClient(HOST, PORT, username='root', password='example')
        self.main_db = client['main_mongo_db']
        self.users = self.main_db['users_collection']

    def add_user(self, user):
        errors = self.check_user_existence(user.username, user.email)
        if errors:
            return errors, None

        user_id = self.users.insert_one({
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'email': user.email,
            'password': user.password,
            'profile_image_url': user.image_url,
        }).inserted_id

        return [], user_id

    def get_user(self, user_id):
        user_dict = self.users.find_one({'_id': ObjectId(user_id)})
        if not user_dict:
            return [UsersError.USER_ID_NOT_EXISTS], None
        user_dict['user_id'] = str(user_dict['_id'])
        return [], User(user_dict)

    def update_user(self, user_id, updates):
        res = self.users.update_one({'_id': ObjectId(user_id)}, {'$set': updates})

        if res.matched_count == 0:
            return [UsersError.USER_ID_NOT_EXISTS], None

        if res.modified_count == 0:
            return [UsersError.NO_CHANGES_MADE], None

        return [], user_id

    def delete_user(self, user_id):
        res = self.users.delete_one({'_id': ObjectId(user_id)})

        if res.deleted_count == 0:
            user = self.users.find_one({'_id': ObjectId(user_id)})
            if not user:
                return [UsersError.USER_ID_NOT_EXISTS], None
            else:
                return [INTERNAL_ERROR], None

        return [], user_id

    def check_user_existence(self, username, email):
        user_with_username = self.users.find_one({'username': username})
        user_with_email = self.users.find_one({'email': email})

        res = []
        if user_with_username:
            res.append(UsersError.USER_WITH_USERNAME_ALREADY_EXISTS)
        if user_with_email:
            res.append(UsersError.USER_WITH_EMAIL_ALREADY_EXISTS)

        return res

