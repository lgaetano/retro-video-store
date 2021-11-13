from app import db
from app.models.customer import Customer
from app.models.rental import Rental
from app.models.video import Video
from flask import Blueprint, jsonify,request, make_response, abort 
from datetime import date, timedelta

rentals_bp = Blueprint("rentals",__name__,url_prefix="/rentals")

def validate_request_body(request_body):
    """Validates request body."""
    mandatory_fields=["customer_id","video_id"]
    for field in mandatory_fields:
        if field not in request_body:
            abort(make_response({"details":f" Request body must include {field}"}, 400))

def validate_video_customer_existence(request_body):
    """Confirms instances of customer and video exist."""
    video= Video.query.get(request_body["video_id"])
    customer = Customer.query.get(request_body["customer_id"])
    
    if not video:
        abort(make_response({"details":f"Video with id number {request_body['video_id']} was not found"},404))
    elif not customer:
        abort(make_response({"details":f"Customer with id number {request_body['customer_id']} was not found"},404))

    return customer, video

@rentals_bp.route("/check-out",methods=["POST"])
def checkout_video():
    """Checks out a video to a customer, creating a new rental instance."""
    request_body = request.get_json()
    
    validate_request_body(request_body)
    validate_video_customer_existence(request_body)

    rental = Rental.query.get((request_body['video_id'], request_body['customer_id']))
    if rental:
        return jsonify({"message":"Could not perform checkout"}),400
        
    # if video.available_inventory == 0:
    #     return jsonify({"message":"Could not perform checkout"}),400
    new_rental= Rental(
        customer_id = request_body["customer_id"],
        video_id = request_body["video_id"],
        checkout_date = date.today()
    )
    db.session.add(new_rental)
    db.session.commit()
    return jsonify(new_rental.checkout_to_dict()),200

@rentals_bp.route("/check-in",methods=["POST"])
def check_in_video():
    """Checks-in a video, deleting a new rental instance."""
    request_body = request.get_json()
    validate_request_body(request_body)
    validate_video_customer_existence(request_body)

    rental = Rental.query.get((request_body["video_id"],request_body["customer_id"]))
    if not rental:
        return jsonify({"message":f"No outstanding rentals for customer {request_body['customer_id']} and video {request_body['video_id']}"}),400
    
    rental.checkout_status = False
    
    db.session.commit() 
    return jsonify(rental.check_in_to_dict()),200