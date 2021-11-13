from app import db
from datetime import datetime #date.timetuple()? POST

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    registered_at = db.Column(db.DateTime)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    videos_checked_out_count = db.Column(db.Integer)
    videos = db.relationship("Video",secondary="rental", backref="customers")
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "registered_at": self.registered_at,
            "postal_code": self.postal_code,
            "phone": self.phone
        }

    def update_from_response(self, data):
        for key, value in data.items():
            # Restricts attribute additions to columns in table
            if key in Customer.__table__.columns.keys():
                setattr(self, key, value)