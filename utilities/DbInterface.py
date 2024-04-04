import base64
#from models.Img import Img
#from models.Tag import Tag
#from models.ImgTags import ImgTags
from models.All import Img, Tag, ImgTags
import app
from db import db
from flask import flash

class DbInterface:
    """handles database storage of images and tags
        img_file_save: save img data as bit data
        update_tags: updates existing img entry with tags, see CaptionTask
    
    """
    def __init__(self) -> None:
        pass
    
    def img_file_save(file_path, uri) -> Img:
        #get file type to accept PNG of JPEGs
        #input: image file, png or jpeg

        #get ext to save properly and read data
        _, ext = file_path.split('.')

        #CREATE IMG OBJECT AND SAVE
        img:Img = Img(name = file_path, img_uri = uri, image_type = ext)
        db.session.add(img)
        db.session.commit()
        return img


    def update_tags(image_id, tags):
        #update an existing image with tags from chatgpt
        #input: list of strings(tags)
        with app.app.app_context():
            img:Img = Img.query.get(image_id)

            #iterate over tags to remove white space and add value to a Tag db object
            for tag_to_add in tags:
                tag = Tag(value = tag_to_add.strip())
                img.tags.append(tag)

            #save in DB
            db.session.add(tag)
            db.session.add(img)
            db.session.commit()
            return
    @staticmethod
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
            success = DbInterface.delete_tags(image)
            if success == False:
                raise Exception('Tags not properly deleted')
            db.session.delete(image)
            db.session.commit()
        except Exception as e:
            flash('Delete operation failed. Please try again.')
            return False
        return True

    
            
    

