from app import db
from app.models.customer import Customer
from app.models.video import Video
from datetime import date, timedelta

class Rental(db.Model):
    video_id = db.Column(db.Integer, db.ForeignKey("video.id"), primary_key=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), primary_key=True, nullable=False)
    due_date = db.Column(db.DateTime)

    def calculate_due_date(self):
        """Calculates due date as seven days from today. """
        today = date.today()
        due_date = str(today + timedelta(days=7))
        return due_date
    
    # def calculate_available_(self):
    #     pass

    def checkout_to_dict(self):
        return {
            "customer_id": self.customer.id,
            "video_id": self.video.id,
            "due_date": self.calculate_due_date(),
            "videos_checked_out_count": 2,
            "available_inventory": 5
        }