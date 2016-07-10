from flask import Blueprint, render_template
from app.plugin import app

home_page_routes = Blueprint('home_page', __name__, template_folder='asset')


@app.route('/')
def home_page():
    return render_template('index.html')
