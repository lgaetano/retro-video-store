from app import db
from app.models.customer import Customer
from app.models.rental import Rental
from app.models.video import Video
from flask import Blueprint, jsonify,request, make_response, abort 

rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

def rentals_validate_input(data):
    """
    Function that validates presence of all mandatory fields, existence
    of customer and video instances, and presence of rental."""
    # Confirm all mandatory fields present
    mandatory_fields = ["customer_id", "video_id"]
    for field in mandatory_fields:
        if field not in data:
            # return jsonify({"message": f"Request must include {field}."}), 400
            abort(make_response({"message": f"Request must include {field}."}, 400))
    
    # Confirm respective instances of Customer and Video exist
    customer = Customer.query.get(data["customer_id"])
    if not customer:
        # return jsonify({"message": f"Could not locate customer {response_body['customer_id']}"}), 404
        abort(make_response({"message": f"Could not locate customer {data['customer_id']}"}, 404))
    video = Video.query.get(data["video_id"])
    if not video:
        # return jsonify({"message": f"Could not locate video {response_body['video_id']}"}), 404
        abort(make_response({"message": f"Could not locate video {data['video_id']}"}, 404))
    
    # Confirm rental does not already exist
    rental = Rental.query.get((customer.id, video.id))

    return rental


@rentals_bp.route("/check-out", methods=["POST"])
def check_out():
    """Checks out a video to a customer and updates the database."""
    response_body = request.get_json()
    rental = rentals_validate_input(response_body)
    
    if rental: # exists
        return jsonify({"message": f"Could not perform checkout"}), 400

    new_rental = Rental(
        customer_id=response_body["customer_id"],
        video_id=response_body["video_id"]
    )
    db.session.add(new_rental)
    db.session.commit()
    
    return jsonify(new_rental.checkout_to_dict()), 200

@rentals_bp.route("/check-in", methods=["POST"])
def check_in():
    """Checks in a video from a customer and updates the database."""
    response_body = request.get_json()

    rental = rentals_validate_input(response_body)
    if not rental:
        return jsonify({"message": f"No outstanding rentals for customer {response_body['customer_id']} and video {response_body['video_id']}"}), 400

    return jsonify(rental.check_in_to_dict()), 200