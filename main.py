from bson import json_util
from flask import Flask, request, Response, render_template
from flask_login import LoginManager, UserMixin, login_user
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
mongo = PyMongo(app)
login_manager = LoginManager(app)


class User(UserMixin):
    def __init__(self, id):
        self.id = id

    @staticmethod
    def get(user_id):
        return User(user_id)


def _mongo_to_json_response(mongo):
    return Response(json_util.dumps(mongo, indent=4, sort_keys=True), mimetype="application/json")


@login_manager.user_loader
def _login_manager_load_user(user_id):
    return User.get(user_id)


@app.route('/')
@app.route('/home')
def home_page():
    videos = mongo.db.videos.find()
    return render_template('home_page.html', videos=videos)


@app.route('/home/video/<int:video_id>/')
def view_video_page(video_id):
    video = mongo.db.videos.find({'video_id': video_id})
    return render_template('video_page.html', video=video)


@app.route('/home/videos/most_recent/')
@app.route('/home/videos/trending/')
def get_newest_video():
    newest_videos = mongo.db.videos.find().sort({'_id':-1}).limit(10)
    return render_template('recent_videos.html', newest_videos=newest_videos)


@app.route('/api/v1/videos/<int:video_id>/comments')
def get_video_comments(video_id):
    return _mongo_to_json_response(mongo.db.comments.find({'video_id': video_id}))


@app.route('/api/v1/videos/<int:video_id>/comments', methods=['POST'])
def post_video_comments(video_id):
    comment = request.get_json()
    comment['video_id'] = video_id
    return _mongo_to_json_response(mongo.db.comments.insert(comment))


@app.route('/home/videos/video_data/<int:video_id>')
def get_video_data(video_id):
    return _mongo_to_json_response(mongo.db.videos.find({'video_id': video_id}))


@app.route('/home/users/<int:user_id>')
def get_user_subscription_videos(user_id):
    subscriptions = mongo.db.users.find({'user_id': user_id}, {'subscriptions': 1})
    return _mongo_to_json_response(mongo.db.subscriptions.find().sort({'_id':-1}))


@app.route('/api/v1/users', methods=['POST'])
def post_user():
    user = request.get_json()
    user['password'] = generate_password_hash(user['password'])
    return _mongo_to_json_response(mongo.db.users.insert(user))


@app.route('/api/v1/users/login', methods=['POST'])
def post_user_login():
    user = request.get_json()
    mongo_user = mongo.db.users.find_one({'name': user['name']})

    if mongo_user and check_password_hash(mongo_user['password'], user['password']):
        login_user(User(mongo_user['_id']))
        return 'Success'
    return 'Failure'


if __name__ == '__main__':
    app.secret_key = 'super_secret_key_that_no_one_can_break_in'
    app.debug = True
    app.run(host='0.0.0.0', port=7000)
