from bson import json_util
from flask import Response


def mongo_to_json_response(mongo):
    return Response(json_util.dumps(mongo, indent=4, sort_keys=True), mimetype="application/json")
