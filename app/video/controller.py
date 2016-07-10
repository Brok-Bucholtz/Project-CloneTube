from flask import Blueprint, request
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os

from app.plugin import app, mongo
from app.helper import mongo_to_json_response


video_api_routes = Blueprint('video_api', __name__)

ALLOWED_EXTENSIONS = set(['mp4', '3gp', 'ogg'])

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


@video_api_routes.route('/videos', methods=['POST'])
@login_required
def upload_video():
    if request.method == 'POST':
        filename = upload_file(current_user.get_id())
        mongo.db.video.insert({'name': request.form['name'], 'user_id': current_user.get_id(), filename: filename})
