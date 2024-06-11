import os
import fasttext.util
from flask import Flask
import fasttext
from db import db
from models.All import Img, Tag, ImgTags
from sqlalchemy import text


app = Flask(__name__)
app.secret_key = os.getenv("SESSION_SECRET_KEY")

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
#Keeping option off for now to save data, may use later for hooks on when captioning tasks complete
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.app_context().push()

db.init_app(app)
print('initiated app')

fasttext_model = fasttext.load_model(r'C:\Users\hughd\Documents\Future Work\Coding Projects\imgcap\imgcap\fasttext\dbpedia.bin')

#needs to be imported after app is initiated
import views


#REMOVED FOR PRODUCTION TO TABLES ARE NOT RECREATED
#with app.app_context():
#    db.drop_all()
#    db.create_all()
db.session.execute(text('CREATE EXTENSION IF NOT EXISTS vector'))
db.session.commit()