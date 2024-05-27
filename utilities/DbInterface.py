from flask import flash
from models.All import Img, Tag, ImgTags
import app
from db import db


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
        tags [Tag] 
    """
    with app.app.app_context():
        img:Img = Img.query.get(image_id)

        for tag_to_add in tags:
            tag = Tag(value = tag_to_add.strip())
            img.tags.append(tag)

        #save in DB
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
    return images_from_tags

def delete_tags(image:Img):
    try:
        for tag in image.tags:
            db.session.delete(tag)
        db.session.commit()
    except Exception as e:
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
        flash('Delete operation failed. Please try again.')
        return False
    return True


        


