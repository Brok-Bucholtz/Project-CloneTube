from bson import json_util
from flask import Flask, request, Response
from flask_pymongo import PyMongo

app = Flask(__name__)
mongo = PyMongo(app)


def _mongo_to_json_response(mongo):
    return Response(json_util.dumps(mongo, indent=4, sort_keys=True), mimetype="application/json")


@app.route('/')
def hello():
    return 'Hello World'


@app.route('/api/v1/videos/<int:video_id>/comments')
def get_video_comments(video_id):
    return _mongo_to_json_response(mongo.db.comments.find({'video_id': video_id}))


@app.route('/api/v1/videos/<int:video_id>/comments', methods=['POST'])
def post_video_comments(video_id):
    comment = request.get_json()
    comment['video_id'] = video_id
    return _mongo_to_json_response(mongo.db.comments.insert(comment))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key_that_no_one_can_break_in'
    app.debug = True
    app.run(host='0.0.0.0', port=7000)
