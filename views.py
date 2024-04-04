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
from utilities.ImageStorageInterface import ImageStorageInterface

from werkzeug.utils import secure_filename


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
    
    #SECURE FILE NAME AGAINST MALICIOUS TEXT
    filename_secured = secure_filename(file.filename)

    #UPLOAD TO AWS AND RETURN URI
    #THEN ADD TO DB
    image_uri = ImageStorageInterface.upload_to_aws(file.read(), filename_secured)
    if image_uri:
        img:Img = DbInterface.img_file_save(filename_secured, image_uri)

    #start image captioning with GPT
    #CREATE NEW THREAD
    task = CaptionTask(image_uri, img.image_type, img.id)
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
    relevant_tags = Tag.query.filter(Tag.value.like(escape(request.values.get('search'))+"%")).all()
    if relevant_tags:
        image_data = []

        #ITERATE OVER ALL TAGS TO GET LINKED IMAGES
        for tag in relevant_tags:
            image_data += tag.images

        #REMOVE DUPLICATE IMAGES WHEN MULTIPLE TAGS POINT TO SAME IMAGE
        image_data = list(set(image_data))
        image_data = [image_data[int(len(image_data)//2):], image_data[:int(len(image_data)//2)]]
    else:
        image_data = []
    
    return render_template('index.html', images=image_data)


@app.route('/image/<int:id>')
def serve_image(id):
    #SERVES IMAGES FOR DISPLAY, PROVIDES IMAGES AS BYTES
    img: Img = Img.query.get(id)
    
    # used for db storage of images, depricated in favor of s3 storage
    # return send_file(io.BytesIO(img.img), mimetype=f'image/{img.image_type}')

    return img.img_uri

@app.route('/delete/<int:id>', methods = ['POST'])
def delete(id):
    #DELETES IMAGES BASED ON ID. IMAGE DELETED FROM DB FIRST THEN REMOVED FROM CDN
    img:Img = Img.query.filter_by(id = id).one()
    success = DbInterface.delete_img(img)
    #ONLY REMOVE FROM CDN IF REMOVED FROM DB TO AVOID IMAGE NOT FOUND ERROR
    if success:
        ImageStorageInterface.delete_from_aws(img.name)
    return redirect(url_for('home'))







if __name__ == '__main__':
   app.run()

