"""Handles all app routing including 
displaying images, uploading images, search and delete"""
from flask import redirect, url_for, render_template, jsonify,flash,request
from flask_sqlalchemy import SQLAlchemy
from psycopg2 import OperationalError
import logging
from app import app
from models.All import Img, Tag, ImgTags
from db import db
import utilities.DbInterface as DbInterface
from utilities.ImageProcessing import process_image, delete_image_and_metadata
from helpers.prep_images_for_display import prep_images_for_display

@app.route("/")
def home():
    """SPLITS IMAGES INTO TWO GROUPS FOR DISPLAY ON TWO COLUMNS ON HOMEPAGE
    TO ADD ORDERING BY DATE ADDED"""
    images = []
    try:
        images = Img.query.all()
        #if no images query will return None type object
        if images is not None:
            images.sort(key=lambda x: x.date_created, reverse=True)
    except OperationalError as e:
        logging.exception(e)
        raise ConnectionError('Unable to connect to server. Please check connection')
    except Exception as e:
        logging.exception(e)
        flash('Could not load images. Please check connection and try again')
        raise ConnectionError('Unable to connect to server. This may be a server issue, please check connection and try again')
    return render_template('index.html', images=images)

@app.route('/upload', methods = ['POST'])
def upload():
    """ENDPOINT FOR POST REQUESTS TO ADD IMAGES TO DB
    CAPTIONING PERFORMED IN DIFFERENT THREAD
    
    next steps: issue of captioning task failing after image upload
    """

    file = request.files['file']
    try:
        process_image(file)
    except Exception as e:
        logging.exception(e)
        flash('Image could not be processed. Please try again')
    return redirect(url_for('home'))

@app.route('/autocomplete')
def autocomplete():
    """RETURNS ALL AVAILABLE TAGS 
    FOR SEARCH BAR AUTOCOMPLETE"""
    tags = []
    try:
        tags = db.session.query(Tag).distinct(Tag.value).all()
        tags = [tag.value for tag in tags]
    except Exception as e:
        logging.exception(e)
    return jsonify(tags)

@app.route('/search', methods = ['GET'])
def search():
    """OBTAIN RELEVANT TAGS, GET ASOCCIATED IMAGES 
    FROM TAGS AND SPLIT INTO TWO LISTS FOR DISPLAY"""
    
    #GET ONLY DISTINCT TAGS TO AVOID DUPLICATE IMAGES
    tags_from_query = DbInterface.get_query_by_tag(request.values.get('search'), 0.9)
    images_from_tags = DbInterface.get_img_from_tag(tags_from_query)
    return render_template('index.html', images=images_from_tags)


@app.route('/image/<int:id>')
def serve_image(image_id):
    """SERVES IMAGE FROM CDN, 
    PROVIDES IMAGES AS URI"""

    img: Img = Img.query.get(image_id)
    return img.img_uri

@app.route('/delete/<int:image_id>', methods = ['POST'])
def delete(image_id):
    """IMAGE DELETED FROM DB FIRST THEN REMOVED FROM CDN TO PREVENT TRYING ACCESS DELETED IMAGE"""

    delete_image_and_metadata(image_id)
    return redirect(url_for('home'))







if __name__ == '__main__':
   app.run()

