from db import db
from sqlalchemy.orm import declarative_base
Base = declarative_base()

ImgTags = db.Table('imgtags', Base.metadata,
    db.Column('image_id', db.Integer, db.ForeignKey('Img.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('Tag.id'))
)


