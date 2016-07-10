from flask import request, render_template, send_from_directory
from werkzeug.utils import secure_filename
import os

from app.app import app, mongo
from app.account.controller import account_page_routes
from app.helper import mongo_to_json_response
from app.authentication.controller import authentication_api_routes, authentication_page_routes
from app.video.newest_videos.controller import new_videos_routes
from app.video.view_video.controller import view_video_routes


app.register_blueprint(account_page_routes, url_prefix='/account')
app.register_blueprint(authentication_page_routes, url_prefix='/authentication')
app.register_blueprint(authentication_api_routes, url_prefix='/api/v1/authentication')
app.register_blueprint(new_videos_routes, url_prefix="/api/v1/video/")
app.register_blueprint(view_video_routes, url_prefix="/api/v1/video/")

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



@app.route('/')
@app.route('/home')
def home_page():
    videos = mongo.db.videos.find()
    return render_template('home_page.html', videos=videos)


@app.route('/api/v1/videos/<int:video_id>/comments')
def get_video_comments(video_id):
    return mongo_to_json_response(mongo.db.comments.find({'video_id': video_id}))


@app.route('/api/v1/videos/<int:video_id>/comments', methods=['POST'])
def post_video_comments(video_id):
    comment = request.get_json()
    comment['video_id'] = video_id
    return mongo_to_json_response(mongo.db.comments.insert(comment))


@app.route('/home/users/<int:user_id>')
def get_user_subscription_videos(user_id):
    subscriptions = mongo.db.users.find({'user_id': user_id}, {'subscriptions': 1})
    return mongo_to_json_response(mongo.db.subscriptions.find().sort({'_id':-1}))


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
