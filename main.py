from bson import json_util
from flask import Flask, request, Response, render_template, send_from_directory
from flask_login import LoginManager, UserMixin, login_user
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)
mongo = PyMongo(app)
login_manager = LoginManager(app)

UPLOAD_FOLDER = 'static/data'
ALLOWED_EXTENSIONS = set(['mp4', '3gp', 'ogg'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def upload_file(user_id):
    f = request.files['video_file']
    if f and allowed_file(f.filename):
        filename = secure_filename(f.filename)
        directory_path = os.path.join(app.config['UPLOAD_FOLDER'], str(user_id))
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        f.save(os.path.join(directory_path, filename))
    return filename



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


@app.route('/app/<path:path>')
def send_js(path):
    return send_from_directory('client', path)


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


@app.route('/home/user/<int:user_id>/upload/', methods=['POST'])
def upload_video(user_id):
    user = mongo.db.users.find_one({'user_id': user_id})
    if request.method == 'POST':
        user['videos'] = mongo.db.video.insert({'name': request.form['name'], 'user_id': user_id})
        if request.files['video_files']:
            filename = upload_file(user_id)
            saved_filename = str(filename)




if __name__ == '__main__':
    app.secret_key = 'super_secret_key_that_no_one_can_break_in'
    app.debug = True
    app.run(host='0.0.0.0', port=7000)
