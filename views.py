from imgcap import app
from flask import render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from models.Img import Img
import os
from utilities.DbStorage import DbStorage
from db import db

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/upload', methods = ['POST'])
#handle img uploading and save to db
def upload():
    print(request.files)
    if request.method == 'POST':
        #check if there is a file
        file = request.files['file']
        if 'file' not in request.files:
            return 'No file found', 400
        file = request.files['file']
        if file.filename == '':
            return 'No selected file', 400
        filename = secure_filename(file.filename)
        file_path = os.path.join('/temp', filename)
        file.save(file_path)


        with open(file_path, 'rb') as f:
            DbStore = DbStorage()
            img = Img(name=filename, img=DbStore.convert_b64(f.read()))
            db.session.add(img)
            db.session.commit()
    return 'File uploaded successfully', 200





if __name__ == '__main__':
   app.run()

