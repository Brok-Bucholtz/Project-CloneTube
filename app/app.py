from flask import Flask
from flask_login import LoginManager
from flask_pymongo import PyMongo

app = Flask('CloneTube')
mongo = PyMongo(app)
login_manager = LoginManager(app)
