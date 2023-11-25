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
from html import escape

from utilities.CaptionTask import CaptionTask 

@app.route("/")
def home():
    images = Img.query.all()
    return render_template('index.html', images=images)

@app.route('/upload', methods = ['POST'])
#handle img uploading and save to db
def upload():
    file = request.files['file']
    #get file type to accept PNG of JPEGs
    file_path = secure_filename(file.filename)
    _, ext = file_path.split('.')

    #DbStore = DbStorage()
    img_data = file.read()
    img:Img = Img(name=file.filename, img=img_data, image_type = ext)
    db.session.add(img)
    db.session.commit()

    #start image captioning with GPT
    task = CaptionTask(img.img, img.image_type, img.id)
    task.start()
    return redirect(url_for('home'))





@app.route('/search', methods = ['GET'])
def search():
    data: Img = Img.query.filter_by(tags = escape(request.values.get('search')))
    return render_template('index.html', images=data)


@app.route('/image/<int:id>')
def serve_image(id):
    img: Img = Img.query.get(id)
    return send_file(io.BytesIO(img.img), mimetype=f'image/{img.image_type}')





if __name__ == '__main__':
   app.run()

