from app.account.controller import account_page_routes, account_api_routes
from app.home.controller import home_page_routes
from app.video.controller import video_api_routes, video_page_routes
from app.video.newest_videos.controller import new_videos_routes
from app.video.view_video.controller import view_video_page_routes


def build_route(app):
    app.register_blueprint(account_page_routes, url_prefix='/account')
    app.register_blueprint(home_page_routes)
    app.register_blueprint(video_page_routes, url_prefix='/video')
    app.register_blueprint(view_video_page_routes, url_prefix='/video')

    app.register_blueprint(account_api_routes, url_prefix='/api/v1')
    app.register_blueprint(video_api_routes, url_prefix='/api/v1')
    app.register_blueprint(new_videos_routes, url_prefix="/api/v1/video/")
