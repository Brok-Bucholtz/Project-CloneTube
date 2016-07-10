from flask import Blueprint, request, render_template
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os

from app.plugin import app, mongo
from app.helper import mongo_to_json_response


video_api_routes = Blueprint('video_api', __name__)
video_page_routes = Blueprint('video_page', __name__, template_folder='asset', static_folder='asset')


def upload_file(file, user_id):
    filename = secure_filename(file.filename)
    directory_path = os.path.join(app.config['UPLOAD_FOLDER'], str(user_id))
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    file.save(os.path.join(directory_path, filename))
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
def post_video():
    title = request.form['title']
    file = request.files['file']
    server_filename = upload_file(file, current_user.get_id())
    video = mongo.db.video.insert({'title': title, 'user_id': current_user.get_id(), 'filename': server_filename})
    return mongo_to_json_response(video)


@video_page_routes.route('/upload')
@login_required
def upload_video():
    return render_template('upload.html')
