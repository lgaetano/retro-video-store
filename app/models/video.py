from app import db

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    total_inventory = db.Column(db.Integer)
    release_date = db.Column(db.DateTime)
    available_inventory = db.Column(db.Integer)
    
    
    def video_dict(self):
        
        return{
            "id":self.id,
            "title":self.title,
            "total_inventory":self.total_inventory,
            "release_date":self.release_date
        }
        
            