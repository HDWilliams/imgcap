from db import db
from sqlalchemy.orm import declarative_base
from sqlalchemy import String, Column, Integer

#INCLUDING ALL DB MODELS IN ONE FILE FOR EASIER LOADING AND CONNECTING TABLES
#ORDER OF IMPORT MATTERS

ImgTags = db.Table('imgtags', db.metadata,
    db.Column('image_id', db.Integer, db.ForeignKey('Img.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('Tag.id'))
)

class Img(db.Model):
    __tablename__ = "Img"

    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    img_uri = Column(String)
    image_type = Column(String(200))
    description = Column(String(200))
    tags = db.relationship('Tag', secondary=ImgTags, backref=db.backref('images'))
    

    def __repr__(self) -> str:
        return '<Img %r>' % self.id
    
class Tag(db.Model):
    __tablename__ = "Tag"
    id = Column(Integer, primary_key=True)
    value = Column(String(200))

    def __repr__(self) -> str:
        return '<Tags %r>' % self.id


