from flask import Flask
from db import db
from models.All import Img, Tag, ImgTags
import os

app = Flask(__name__)

#establish directory for the test db
basedir = os.path.abspath(os.path.dirname(__file__))

#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///temp.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.app_context().push()

#initiate db
db.init_app(app)
with app.app_context():
    db.drop_all()
    db.create_all()

import views