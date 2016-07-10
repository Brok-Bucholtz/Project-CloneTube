from flask import Blueprint, render_template
from app.plugin import mongo


view_video_page_routes = Blueprint('view_video_page', __name__, template_folder='assets', static_folder='assets')


@view_video_page_routes.route('/view_videos')
def view_video_page(video_id):
    video = mongo.db.videos.find({'video_id': video_id})
    return render_template('video_page.html', video=video)
