from app import app
from flask import send_file, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from models.Img import Img
import os
from utilities.DbStorage import DbStorage
from db import db
import io

import base64

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/upload', methods = ['POST'])
#handle img uploading and save to db
def upload():
    file = request.files['file']
    #DbStore = DbStorage()
    encoded_data = base64.b64encode(file.read()).decode('ascii')
    img:Img = Img(name=file.filename, img=encoded_data)
    print(f"Stored data: {len(img.img)}")
    db.session.add(img)
    db.session.commit()
    return redirect(url_for('display'))

@app.route('/display')
def display():
    file: Img = Img.query.first()
    print(f"Retrieved data: {len(file.img)}")
    if file.img is not None:
        return render_template('display.html', image_data = file.img)
    else:
        return 'Image Not Found', 404






if __name__ == '__main__':
   app.run()

