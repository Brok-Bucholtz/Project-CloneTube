from flask_login import LoginManager
from flask_pymongo import PyMongo

from app.app import app

mongo = PyMongo(app)
login_manager = LoginManager(app)
