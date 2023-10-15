from flask import Flask
from db import db
import os

app = Flask(__name__)

#establish directory for the test db
basedir = os.path.abspath(os.path.dirname(__file__))

#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.app_context().push()

#initiate db
db.init_app(app)
db.create_all()

import views