from app import db
from flask import Blueprint, jsonify,request, make_response, abort 
from app.models.customer import Customer
from app.models.rental import Rental
from app.models.video import Video
import utils.customer_validations as val
from datetime import date, datetime, timezone

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")

def validate_endpoint_id(id, param_id):
    """Validates id for endpoint is an integer."""
    try:
        int(id)
    except:
        abort(make_response({f"details": "{param_id} must be an int."}, 400))

def timestamp():
    """
    Determines current time and formats to specficiation.
    e.g. "Wed, 16 Apr 2014 21:40:20 -0700"""
    #TODO: fix datetime formatting
    now = datetime.now(timezone.utc).astimezone().strftime("%a, %d %b %Y %H:%M:%S %z")
    print(now) # Sat, 06 Nov 2021 21:37:21 -0700 (DOESN'T PRINT THIS WAY IN POSTMAN)
    return now

#WHY DID I HHAVE TO DO val.validate_customer_instance(customer_id)... TO IMPORT THIS!?
# DIDN"T WORK AS from ... impor validate_cust...

@customers_bp.route("", methods=["GET"])
def get_all_customer():
    """Retrieves all customers from database."""
    customers = Customer.query.all()
    return jsonify([customer.to_dict() for customer in customers]), 200

@customers_bp.route("<customer_id>", methods=["GET"])
def get_customer_by_id(customer_id):
    """Retreives customer data by id."""
    validate_endpoint_id(customer_id, "customer_id")
    customer = val.validate_customer_instance(customer_id)
    return jsonify(customer.to_dict())

@customers_bp.route("", methods=["POST"])
def create_customer():
    """Creates a customer from JSON user input."""
    response_body = request.get_json()
    val.validate_form_data(response_body)

    if not val.validate_postal_code(response_body["postal_code"]):
        return jsonify({"details": "Invalid format for postal_code."}), 400
    if not val.validate_phone_number(response_body["phone"]):
        return jsonify({"details": "Invalid format for phone number."}), 400

    new_customer = Customer(
        name=response_body["name"],
        registered_at=timestamp(),
        postal_code=response_body["postal_code"],
        phone=response_body["phone"]
    )

    db.session.add(new_customer)
    db.session.commit()
    return jsonify({"id": new_customer.id}), 201

@customers_bp.route("<customer_id>", methods=["PUT"])
def update_customer_by_id(customer_id):
    """Updates all customer data by id"""
    customer = val.validate_customer_instance(customer_id)

    response_body = request.get_json()
    val.validate_form_data(response_body)

    customer.update_from_response(response_body)
    db.session.commit()

    return jsonify(customer.to_dict()), 200

@customers_bp.route("<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    """Deletes customer account by id."""
    customer = val.validate_customer_instance(customer_id)
    db.session.delete(customer)
    db.session.commit()

    return jsonify({"id": customer.id}), 200


@customers_bp.route("<customer_id>/rentals", methods=["GET"])
def get_rentals_by_customer_id(customer_id):
    validate_endpoint_id(customer_id, "customer_id")
    val.validate_customer_instance(customer_id)

    results = db.session.query(Rental, Customer, Video) \
                        .select_from(Rental).join(Customer).join(Video).all()
    
    response = []
    for rental, customer, video in results:
        response.append({
            "release_date": video.release_date,
            "title": video.title,
            "due_date": rental.due_date,
    })
        
    return jsonify(response), 200