from app import db
from app.models.customer import Customer
from app.models.rental import Rental
from app.models.video import Video
from flask import Blueprint, jsonify,request, make_response, abort 

rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

def validate_request_body(form_data):
    """Validates request body."""
    mandatory_fields = ["customer_id", "video_id"]
    for field in mandatory_fields:
        if field not in form_data:
            abort(make_response({"message": f"Request must include {field}."}, 400))

def validate_customer_and_video_instances(data):
    """
    Function that validates existence of customer and video instances, 
    returns rental object."""
    customer = Customer.query.get(data["customer_id"])
    if not customer:
        abort(make_response({"message": f"Could not locate customer {data['customer_id']}"}, 404))
    
    video = Video.query.get(data["video_id"])
    if not video:
        abort(make_response({"message": f"Could not locate video {data['video_id']}"}, 404))
    
    # Confirm rental does not already exist
    rental = Rental.query.get((customer.id, video.id))

    return rental


@rentals_bp.route("/check-out", methods=["POST"])
def check_out():
    """Checks out a video to a customer and updates the database."""
    form_data = request.get_json()
    validate_request_body(form_data)

    rental = validate_customer_and_video_instances(form_data)
    if rental: # exists
        return jsonify({"message": f"Could not perform checkout"}), 400

    new_rental = Rental(
        customer_id=form_data["customer_id"],
        video_id=form_data["video_id"]
    )
    db.session.add(new_rental)
    db.session.commit()
    
    return jsonify(new_rental.checkout_to_dict()), 200

@rentals_bp.route("/check-in", methods=["POST"])
def check_in():
    """Checks in a video from a customer and updates the database."""
    form_data = request.get_json()
    validate_request_body(form_data)

    rental = validate_customer_and_video_instances(form_data)
    if not rental:
        return jsonify({"message": f"No outstanding rentals for customer {form_data['customer_id']} and video {form_data['video_id']}"}), 400

    # Remove rental from database
    db.session.delete(rental)
    db.session.commit()
    return jsonify(rental.check_in_to_dict()), 200