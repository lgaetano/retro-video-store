from app import db
from datetime import datetime #date.timetuple()? POST

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    registered_at = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    # videos = db.Column(db.ForeignKey)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "registered_at": self.registered_at,
            "postal_code": self.postal_code,
            "phone": self.phone
        }