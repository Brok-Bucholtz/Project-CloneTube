from flask import Blueprint, request
from werkzeug.utils import secure_filename
import os

from app.app import app, mongo
from app.helper import mongo_to_json_response


video_api_routes = Blueprint('video_api', __name__)

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


@video_api_routes.route('/videos/<int:video_id>/comments')
def get_video_comments(video_id):
    return mongo_to_json_response(mongo.db.comments.find({'video_id': video_id}))


@video_api_routes.route('/videos/<int:video_id>/comments', methods=['POST'])
def post_video_comments(video_id):
    comment = request.get_json()
    comment['video_id'] = video_id
    return mongo_to_json_response(mongo.db.comments.insert(comment))
