from app import db

class Rental(db.Model):
    video_id = db.Column(db.Integer, db.ForeignKey("video.id"), primary_key=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), primary_key=True, nullable=False)
    