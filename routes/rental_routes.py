from app import db
from app.models.customer import Customer
from app.models.rental import Rental
from app.models.video import Video
from flask import Blueprint, jsonify,request, make_response, abort 

rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

@rentals_bp.route("/check-out", methods=["POST"])
def checkout():
    """Checksout a video to a customer and updates the database."""
    response_body = request.get_json()

    # Confirm all mandatory fields present
    mandatory_fields = ["customer_id", "video_id"]
    for field in mandatory_fields:
        if field not in response_body:
            return jsonify({"message": f"Request must include {field}."}), 400
    
    # Confirm respective instances of Customer and Video exist
    customer = Customer.query.get(response_body["customer_id"])
    if not customer:
        return jsonify({"message": f"Could not locate customer {response_body['customer_id']}"}), 404
    video = Video.query.get(response_body["video_id"])
    if not video:
        return jsonify({"message": f"Could not locate video {response_body['video_id']}"}), 404
    
    # Confirm rental does not already exist
    rental = Rental.query.get((customer.id, video.id))
    if rental: # exists
        return jsonify({"message": f"Could not perform checkout"}), 400

    new_rental = Rental(
        customer_id=response_body["customer_id"],
        video_id=response_body["video_id"]
    )
    db.session.add(new_rental)
    db.session.commit()
    
    return jsonify(new_rental.checkout_to_dict()), 200