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
    file = request.files['image']
    #DbStore = DbStorage()
    img:Img = Img(name=file.filename, img=file.read())
    print(len(file.read()))
    db.session.add(img)
    db.session.commit()
        
    return redirect(url_for('display'))

@app.route('/display')
def display():
    file: Img = Img.query.first()
    
    image_data = base64.b64encode(file.img).decode('ascii')
    if image_data is not None:
        return render_template('display.html', image_data = image_data)
    else:
        return 'Image Not Found', 404






if __name__ == '__main__':
   app.run()

