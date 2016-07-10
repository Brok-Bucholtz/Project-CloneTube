from flask import Blueprint
from app.plugin import app

home_page_routes = Blueprint('home_page', __name__)


@app.route('/')
def home_page():
    return "Welcome!"
