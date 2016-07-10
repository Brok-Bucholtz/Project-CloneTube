from flask import Blueprint, request
from flask_login import UserMixin, login_user
from werkzeug.security import generate_password_hash, check_password_hash

from app.app import login_manager, mongo
from app.helper import mongo_to_json_response

authentication_api_routes = Blueprint('authentication_api', __name__, template_folder='.')


class User(UserMixin):
    def __init__(self, id):
        self.id = id

    @staticmethod
    def get(user_id):
        return User(user_id)


@login_manager.user_loader
def _login_manager_load_user(user_id):
    return User.get(user_id)


@authentication_api_routes.route('/users', methods=['POST'])
def post_user():
    user = request.get_json()
    user['password'] = generate_password_hash(user['password'])
    return mongo_to_json_response(mongo.db.users.insert(user))


@authentication_api_routes.route('/users/login', methods=['POST'])
def post_user_login():
    user = request.get_json()
    mongo_user = mongo.db.users.find_one({'name': user['name']})

    if mongo_user and check_password_hash(mongo_user['password'], user['password']):
        login_user(User(mongo_user['_id']))
        return 'Success'
    return 'Failure'
