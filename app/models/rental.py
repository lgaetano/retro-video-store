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

    def get_checked_out_count_for_specific_video(self, video_id):
        rentals = Rental.query.filter_by(video_id=video_id)
        return rentals.count()

    def get_avail_inventory_for_specific_video(self, video_id):
        video = Video.query.get(video_id)
        return video.total_inventory - self.get_checked_out_count_for_specific_video(video_id)

    def checkout_to_dict(self):
        """Returns dictionary for rentals/check-out route."""
        return {
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "due_date": self.calculate_due_date(),
            "videos_checked_out_count": self.get_checked_out_count_for_specific_video(self.video_id),
            "available_inventory": self.get_avail_inventory_for_specific_video(self.video_id)
        }

    def check_in_to_dict(self):
        """Returns dictionary for rentals/check-in route."""
        return {
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "videos_checked_out_count": Customer.videos_checked_out_count,
            "available_inventory": Video.total_inventory - Customer.videos_checked_out_count
        }