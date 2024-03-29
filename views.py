from app import app
from flask import send_file, redirect, url_for, render_template, jsonify, request
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
    #HOME ROUTE USED TO DISPLAY EXISITNG IMAGES AND ADD NEW IMAGES
    images = Img.query.all()
    images = [images[int(len(images)//2):],images[:int(len(images)//2)]]
    return render_template('index.html', images=images)

@app.route('/upload', methods = ['POST'])
def upload():
    #ENDPOINT FOR POST REQUESTS TO ADD IMAGES TO DB
    #REDIRECTS TO HOME PAGE UPON COMPLETION

    #GET FILE
    file = request.files['file']


    db_interface = DbInterface()
    img:Img = db_interface.img_file_save(file)

    #start image captioning with GPT
    #CREATE NEW THREAD
    task = CaptionTask(img.img, img.image_type, img.id)
    task.start()
    return redirect(url_for('home'))

@app.route('/autocomplete')
def autocomplete():
    #RETURNS ALL AVAILABLE TAGS FOR
    tags = db.session.query(Tag).all()
    tags = [tag.value for tag in tags]
    return jsonify(tags)

@app.route('/search', methods = ['GET'])
def search():
    #OBTAIN RELEVANT TAGS, GET ASOCCIATED IMAGES FROM TAGS AND SPLIT INTO TWO LISTS FOR DISPLAY
    relevant_tags = Tag.query.filter_by(value=escape(request.values.get('search'))).all()
    if relevant_tags:
        image_data = []
        for tag in relevant_tags:
            image_data += tag.images
        image_data = [image_data[int(len(image_data)//2):], image_data[:int(len(image_data)//2)]]
    else:
        image_data = []
    
    return render_template('index.html', images=image_data)


@app.route('/image/<int:id>')
def serve_image(id):
    #SERVES IMAGES FOR DISPLAY, PROVIDES IMAGES AS BYTES
    img: Img = Img.query.get(id)
    return send_file(io.BytesIO(img.img), mimetype=f'image/{img.image_type}')





if __name__ == '__main__':
   app.run()

