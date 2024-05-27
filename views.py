"""Handles all app routing including 
displaying images, uploading images, search and delete"""

import datetime
from html import escape
import os
from flask import redirect, url_for, render_template, jsonify, request
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from app import app
from models.All import Img, Tag, ImgTags
from db import db
import utilities.DbInterface as DbInterface
from utilities.CaptionTask import CaptionTask
import utilities.StorageInterface as StorageInterface

@app.route("/")
def home():
    """SPLITS IMAGES INTO TWO GROUPS FOR DISPLAY ON TWO COLUMNS ON HOMEPAGE
    TO ADD ORDERING BY DATE ADDED"""
    images = Img.query.all()
    images = [images[int(len(images)//2):],images[:int(len(images)//2)]]
    return render_template('index.html', images=images)

@app.route('/upload', methods = ['POST'])
def upload():
    """ENDPOINT FOR POST REQUESTS TO ADD IMAGES TO DB
    CAPTIONING PERFORMED IN DIFFERENT THREAD
    
    next steps: issue of captioning task failing after image upload
    """

    file = request.files['file']
    filename_secured = secure_filename(file.filename)
    image_uri = StorageInterface.upload_to_aws(file.read(), filename_secured)
    if image_uri:
        img:Img = DbInterface.save_img(filename_secured, image_uri)

    #BEGIN IMAGE CAPTIONING, AS OF 05/2024 USING CHATGPT FOR CAPTIONING
    task = CaptionTask(image_uri, img.image_type, img.id)
    task.start()
    return redirect(url_for('home'))

@app.route('/autocomplete')
def autocomplete():
    """RETURNS ALL AVAILABLE TAGS 
    FOR SEARCH BAR AUTOCOMPLETE"""

    tags = db.session.query(Tag).all()
    tags = [tag.value for tag in tags]
    return jsonify(tags)

@app.route('/search', methods = ['GET'])
def search():
    """OBTAIN RELEVANT TAGS, GET ASOCCIATED IMAGES 
    FROM TAGS AND SPLIT INTO TWO LISTS FOR DISPLAY"""
    
    #GET ONLY DISTINCT TAGS TO AVOID DUPLICATE IMAGES
    tags_from_query = Tag.query.distinct(Tag.value).filter(Tag.value.like(escape(request.values.get('search')) + "%")).all()
    
    images_from_tags = DbInterface.get_img_from_tag(tags_from_query)

    two_column_images = [images_from_tags[int(len(images_from_tags)//2):], images_from_tags[:int(len(images_from_tags)//2)]]
    return render_template('index.html', images=two_column_images)


@app.route('/image/<int:id>')
def serve_image(image_id):
    """SERVES IMAGE FROM CDN, 
    PROVIDES IMAGES AS URI"""
   
    img: Img = Img.query.get(image_id)
    return img.img_uri

@app.route('/delete/<int:image_id>', methods = ['POST'])
def delete(image_id):
    """IMAGE DELETED FROM DB FIRST THEN REMOVED FROM CDN TO PREVENT TRYING ACCESS DELETED IMAGE"""

    img:Img = Img.query.filter_by(id = image_id).one()
    is_deleted_from_db = DbInterface.delete_img(img)
    if is_deleted_from_db:
        StorageInterface.delete_from_aws(img.name)
    return redirect(url_for('home'))







if __name__ == '__main__':
   app.run(debug=True)

