import base64
import models.Img as Img
from db import db

class DbStorage:
    """handles database storage of images and text
    methods:
        convert_base64
        img_save
        text_save
    
    """
    def __init__(self, data = None, user_id = None, img_name = None, img_id = None) -> None:
        self.data = data
        self.user_id = user_id
        self.img_id = img_id
        self.img_name = img_name

    def convert_b64(self, img_decoded) -> str:
        return base64.b64decode(img_decoded)
    
    def img_save(self, data) -> None:
        """"""
        img_b64 = self.convert_b64(data)
        img_db = Img(name = self.img_name, img = img_b64)
        db.session.add(img_db)
        db.session.commit()
        return


    def text_save(self) -> None:
        pass
    

