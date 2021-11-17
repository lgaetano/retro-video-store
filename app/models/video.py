from app import db

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    total_inventory = db.Column(db.Integer)
    release_date = db.Column(db.DateTime)
    available_inventory = db.Column(db.Integer)
    
    @classmethod
    def from_dict(cls, values):
        return cls(**values)

    def video_dict(self):
        return{
            "id":self.id,
            "title":self.title,
            "total_inventory":self.total_inventory,
            "release_date":self.release_date
        }

    def updates_from_dict(self, data):
        """
        Updates attributes from user data, restricting access to attributes
        that are columns."""
        for key, value in data.items():
            if key in Video.__table__.columns.keys():
                setattr(self, key, value)
