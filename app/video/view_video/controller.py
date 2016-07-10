from flask import Blueprint, render_template

from app.plugin import mongo
from app.helper import mongo_to_json_response

view_video_routes = Blueprint('view_videos', __name__, template_folder='.')


def get_video_data(video_id):
    return mongo_to_json_response(mongo.db.videos.find({'video_id': video_id}))


@view_video_routes.route('/view_videos')
def view_video_page(video_id):
    video = mongo.db.videos.find({'video_id': video_id})
    return render_template('video_page.html', video=video)
