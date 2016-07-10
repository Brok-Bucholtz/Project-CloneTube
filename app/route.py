from flask import render_template

from app.account.controller import account_page_routes, account_api_routes
from app.app import app, mongo
from app.video.controller import video_api_routes
from app.video.newest_videos.controller import new_videos_routes
from app.video.view_video.controller import view_video_routes

app.register_blueprint(account_page_routes, url_prefix='/account')
app.register_blueprint(account_api_routes, url_prefix='/api/v1')
app.register_blueprint(video_api_routes, url_prefix='/api/v1')
app.register_blueprint(new_videos_routes, url_prefix="/api/v1/video/")
app.register_blueprint(view_video_routes, url_prefix="/api/v1/video/")


@app.route('/')
@app.route('/home')
def home_page():
    videos = mongo.db.videos.find()
    return render_template('home_page.html', videos=videos)
