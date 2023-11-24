from db import db
from sqlalchemy import String, Column, Integer

class Img(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    img = Column(String)
    image_type = Column(String(200))
    description = Column(String(200))
    tags = Column(String(200))

    def __repr__(self) -> str:
        return '<Img %r>' % self.id
    
