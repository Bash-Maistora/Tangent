from flask import jsonify
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Comment(db.Model):
    __tablename__ = 'comments'

    sku = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(255))
    tone = db.Column(db.String(255))
    created = db.Column(db.DateTime, default=db.func.current_timestamp())


    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        return {'sku': self.sku, 'comment': self.comment, 'tone': self.tone, 'date': self.created}