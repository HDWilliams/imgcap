from flask import Flask
from db import db
from models.All import Img, Tag, ImgTags
import os

app = Flask(__name__)
app.secret_key = os.getenv("SESSION_SECRET_KEY")

#establish directory for the test db
basedir = os.path.abspath(os.path.dirname(__file__))

#Database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
#Keeping option on for now to save data, may use later for hooks on when captioning tasks complete
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.app_context().push()

#initiate db
db.init_app(app)
"""
REMOVED FOR PRODUCTION TO TABLES ARE NOT RECREATED
with app.app_context():
    db.drop_all()
    db.create_all()
"""
import views