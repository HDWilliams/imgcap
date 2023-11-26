import base64
from models.Img import Img
from models.Tag import Tag
from models.ImgTags import ImgTags
import app
from db import db
from werkzeug.utils import secure_filename

class DbInterface:
    """handles database storage of images and text
    methods:
        convert_base64
        img_save
        text_save
    
    """
    def __init__(self) -> None:
        pass
    
    def img_file_save(self, file) -> Img:
        #get file type to accept PNG of JPEGs
        file_path = secure_filename(file.filename)
        _, ext = file_path.split('.')
        data = file.read()
        img:Img = Img(name = file_path, img = data, image_type = ext)
        db.session.add(img)
        db.session.commit()
        return img


    def update_tags(self, image_id, tag):
        with app.app.app_context():
            tag = Tag(value = tag)
            db.session.add(tag)
            db.session.commit()
            tag.parent.append(image_id)
            db.session.commit()
            return
    

