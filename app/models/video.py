from app import db

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    total_inventory = db.Column(db.Integer)
    release_date = db.Column(db.DateTime)

    def to_dict(self):
        return{
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.inventory
        }
