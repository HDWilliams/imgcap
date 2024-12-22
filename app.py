import os
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from db import db
from models.All import Img, Tag, ImgTags #NEED TO BE IMPORTED TO BE RECOG. BY APP
from sqlalchemy import text
import redis

app = Flask(__name__)

#LIMITER IS WIP
host='memcached-14876.c14.us-east-1-3.ec2.redns.redis-cloud.com',
port=14876
username=os.getenv("MEMCACHEDCLOUD_USERNAME"),
password=os.getenv("MEMCACHEDCLOUD_PASSWORD"),

#FLASK LIMITER SETUP
storage_uri = f"redis://{os.getenv('MEMCACHEDCLOUD_USERNAME')}:{os.getenv('MEMCACHEDCLOUD_PASSWORD')}@{os.getenv('MEMCACHEDCLOUD_SERVERS')}"

# Flask-Limiter Setup using Memcached as the storage, FURTHER WORK ON IMPLEMENTING TLS SECURITY 
limiter = Limiter(
    get_remote_address,
    app=app,
    storage_uri=storage_uri,
)
limiter.default_limits = ["20 per minute"]

app.secret_key = os.getenv("SESSION_SECRET_KEY")

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
#Keeping option off for now to save data, may use later for hooks on when captioning tasks complete
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.app_context().push()

db.init_app(app)

#needs to be imported after app is initiated
import views

db.session.execute(text('CREATE EXTENSION IF NOT EXISTS vector'))
db.session.commit()