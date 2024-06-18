import os
from flask import flash
from html import escape
from sqlalchemy import select, func
from models.All import Img, Tag
from models.All import ImgTags
import app
from db import db
import logging
from utilities.get_embeddings import get_embeddings


def save_img(file_path, uri) -> Img:
    """ saves png or jpeg files to database once added to CDN"""
    #get file type to accept PNG of JPEGs
    #input: image file, png or jpeg

    _, ext = file_path.split('.')

    img:Img = Img(name = file_path, img_uri = uri, image_type = ext)
    db.session.add(img)
    db.session.commit()
    return img

def update_tags(image_id, tags):
    """update an existing image with tags from chatgpt
    Args:
        image_id str
        tags [Tag] 
    """
    with app.app.app_context():
        img:Img = Img.query.get(image_id)

        for tag_to_add in tags:
            #split in the case of multi word tags, each is added individually
            tag = Tag(value = tag_to_add, embedding = get_embeddings(tag_to_add)[0][1])
            img.tags.append(tag)
            db.session.add(tag)
        db.session.add(img)
        db.session.commit()
    return
def get_img_from_tag(tags:list):
    """ get related images to a given list of tags"""
    images_from_tags = []

    if tags:
        for tag in tags:
            images_from_tags += tag.images
    #REVIEW FOR MORE OPTIMAL SOLUTION USING ONLY SQL QUERY FILTERING
    return list(set(images_from_tags))

def delete_tags(image:Img):
    try:
        for tag in image.tags:
            db.session.delete(tag)
        db.session.commit()
    except Exception as e:
        logging.exception(e)
        flash("Failed to delete image tags. Please try again.")
        return False
    return True
    
def delete_img(image:Img):
    """DELETE IMAGE FROM DATABASE, BEFORE DELETION FROM CDN
    RETURNS TRUE ON SUCCESS AND FALSE ON FAILURE    
    """

    try:
        success = delete_tags(image)
        if success == False:
            raise Exception('Tags not properly deleted')
        db.session.delete(image)
        db.session.commit()
    except Exception as e:
        logging.exception(e)
        flash('Delete operation failed. Please try again.')
        return False
    return True

def get_query_by_tag(search_query, search_l2_threshold):
    """OBTAIN RELEVANT TAGS FROM SEARCH QUERY
    Args:
        search_query(str): query from request
    return:
        list of tags
        [] if exception
    """
    try:
        tags_from_query = Tag.query.where(Tag.embedding.l2_distance(get_embeddings(search_query)[0][1]) < search_l2_threshold)
        #tags_from_query = Tag.query.distinct(Tag.value).filter(Tag.value.like(escape(search_query.lower()) + "%")).all()
    except FileNotFoundError:
        return []
    except Exception as e:
        logging.exception(e)
    return tags_from_query


        


