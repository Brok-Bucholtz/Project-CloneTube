from flask import Blueprint, request, render_template
from flask_login import UserMixin, login_user
from werkzeug.security import generate_password_hash, check_password_hash

from app.app import login_manager, mongo
from app.helper import mongo_to_json_response

account_api_routes = Blueprint('account_api', __name__)
account_page_routes = Blueprint('account_page', __name__, template_folder='asset', static_folder='asset')


class User(UserMixin):
    def __init__(self, id):
        self.id = id

    @staticmethod
    def get(user_id):
        return User(user_id)


@login_manager.user_loader
def _login_manager_load_user(user_id):
    return User.get(user_id)


@account_api_routes.route('/accounts', methods=['POST'])
def post_user():
    user = request.get_json()
    user['password'] = generate_password_hash(user['password'])
    return mongo_to_json_response(mongo.db.users.insert(user))


@account_api_routes.route('/accounts/login', methods=['POST'])
def post_user_login():
    user = request.get_json()
    mongo_user = mongo.db.users.find_one({'username': user['username']})

    if mongo_user and check_password_hash(mongo_user['password'], user['password']):
        login_user(User(mongo_user['_id']))
        return 'Success'
    return 'Failure'


@account_page_routes.route('/login')
def login():
    return render_template('login.html')


@account_page_routes.route('/create')
def create_account():
    return render_template('create.html')
