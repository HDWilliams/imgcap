from db import db
from sqlalchemy import Column, Integer, String
from models.ImgTags import ImgTags


class Tag(db.Model):
    __tablename__ = "Tag"
    id = Column(Integer, primary_key=True)
    images = db.relationship('Img', secondary=ImgTags, backref=db.backref('tags'))
    value = Column(String(200))

    def __repr__(self) -> str:
        return '<Tags %r>' % self.id