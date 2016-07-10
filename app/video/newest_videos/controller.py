from flask import Blueprint, render_template

from app.app import mongo

new_videos_routes = Blueprint('newest_videos', __name__, template_folder='.')


@new_videos_routes.route("/newest_videos")
def get_newest_video():
    newest_videos = mongo.db.videos.find().sort({'_id':-1}).limit(10)
    return render_template('newest_videos.html', newest_videos=newest_videos)
