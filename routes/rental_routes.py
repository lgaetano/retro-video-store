from app import db
from app.models.customer import Customer
from app.models.rental import Rental
from app.models.video import Video
from flask import Blueprint, jsonify,request, make_response, abort 

rentals_bp = Blueprint("rentals",__name__,url_prefix="/rentals")

@rentals_bp.route("",methods=["POST"])
def checkout_video():
    request_body = request.get_json()
    new_rental= Rental(
        customer_id = request_body["customer_id"],
        video_id = request_body["video_id"]
    )
    db.session.add(new_rental)
    db.session.commit()
    return jsonify(new_rental.checkout_to_dict()),200