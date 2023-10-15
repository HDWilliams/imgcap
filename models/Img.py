from db import db


class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    img = db.Column(db.LargeBinary)
    description = db.Column(db.String(200))
    tags = db.Column(db.String(200))

    def __repr__(self) -> str:
        return '<Img %r>' % self.id
    
