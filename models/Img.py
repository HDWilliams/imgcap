from db import db
from sqlalchemy import String, Column, Integer
from models.ImgTags import ImgTags


class Img(db.Model):
    __tablename__ = "Img"

    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    img = Column(String)
    image_type = Column(String(200))
    description = Column(String(200))
    tags = db.relationship('Tag', secondary=ImgTags, backref=db.backref('images'))
    

    def __repr__(self) -> str:
        return '<Img %r>' % self.id
    
