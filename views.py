from app import app
from flask import send_file, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy

#from models.Img import Img
#from models.Tag import Tag
#from models.ImgTags import ImgTags
from models.All import Img, Tag, ImgTags
import os
from utilities.DbInterface import DbInterface
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
    

    db_interface = DbInterface()
    img:Img = db_interface.img_file_save(file)

    #start image captioning with GPT
    task = CaptionTask(img.img, img.image_type, img.id)
    task.start()
    return redirect(url_for('home'))





@app.route('/search', methods = ['GET'])
def search():
    relevant_tags = Tag.query.filter_by(value=escape(request.values.get('search'))).first()
    print(relevant_tags)
    if relevant_tags:
        print(relevant_tags.value)
        image_data = [image for image in relevant_tags.images]
    else:
        image_data = []
    
    return render_template('index.html', images=image_data)


@app.route('/image/<int:id>')
def serve_image(id):
    img: Img = Img.query.get(id)
    return send_file(io.BytesIO(img.img), mimetype=f'image/{img.image_type}')





if __name__ == '__main__':
   app.run()

