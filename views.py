from app import app
from flask import send_file, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from models.Img import Img
import os
from utilities.DbStorage import DbStorage
from db import db
import io
import datetime

import base64

@app.route("/")
def home():
    images = Img.query.all()
    return render_template('index.html', images=images)

@app.route('/upload', methods = ['POST'])
#handle img uploading and save to db
def upload():
    file = request.files['file']
    #DbStore = DbStorage()
    img_data = file.read()
    img:Img = Img(name=file.filename, img=img_data)
    print(f"Stored data: {len(img.img)}")
    db.session.add(img)
    db.session.commit()
    return redirect(url_for('home'))





@app.route('/search', methods = ['GET'])
def search():
    data: Img = Img.query.filter_by(tags = request.values.get('search'))
    return render_template('index.html', images=data)


@app.route('/image/<int:id>')
def serve_image(id):
    image: Img = Img.query.get(id)
    return send_file(io.BytesIO(image.img), mimetype='image/jpeg')





if __name__ == '__main__':
   app.run()

