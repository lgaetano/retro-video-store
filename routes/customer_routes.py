from app import db
from app.models.customer import Customer
from app.models.rental import Rental
from app.models.video import Video
from flask import Blueprint, jsonify,request, make_response, abort 
from datetime import date, datetime, timezone
import re

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")

def timestamp():
    """
    Determines current time and formats to specficiation.
    e.g. "Wed, 16 Apr 2014 21:40:20 -0700"""
    #TODO: fix datetime formatting
    #TODO: Should this go here? Customer method?
    # now = datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z")
    now = datetime.now(timezone.utc).astimezone().strftime("%a, %d %b %Y %H:%M:%S %z")
    print(now) # Sat, 06 Nov 2021 21:37:21 -0700 (DOESN'T PRINT THIS WAY IN POSTMAN)
    return now

def validate_id(id):
    """Validates id for endpoint is an integer."""
    try:
        int(id)
    except:
        return abort(jsonify({"details": "Id must be an int."}), 400)

#TODO: SHOULD FLASK METHODS BE COMPLETELY EMPTY FROM MODELS??
def validate_phone_number(phone_num):
    """Uses regex to confirm phone data matches standard US phone number."""
    basic_phone_num = re.compile("(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4})")
    if re.fullmatch(basic_phone_num, phone_num):
        return True
    return False

def validate_postal_code(postal_code):
    """Uses regex to confirm zipcode data matches standard US zipcode."""
    basic_zipcode = re.compile("\d{5}")
    if re.fullmatch(basic_zipcode, postal_code):
        return True
    return False

@customers_bp.route("", methods=["GET"])
def get_all_customer():
    """Retrieves all customers from database."""
    customers = Customer.query.all()

    return jsonify([customer.to_dict() for customer in customers]), 200

@customers_bp.route("<customer_id>", methods=["GET"])
def get_customer_by_id(customer_id):
    """Retreives customer data by id."""
    # TODO: ID VALIDATION DECORATOR
    validate_id(customer_id)
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({"message": f"Customer {customer_id} was not found"}), 404

    return jsonify(customer.to_dict())

@customers_bp.route("", methods=["POST"])
def create_customer():
    """Creates a customer from JSON user input."""
    response_body = request.get_json()
    
    #TODO: VALID INPUT DECORATOR FOR PUT/POST
    mandatory_fields = ["name", "postal_code", "phone"]
    for field in mandatory_fields:
        if field not in response_body:
            return jsonify({"details": f"Request body must include {field}."}), 400
        elif field == "postal_code":
            if not validate_postal_code(response_body["postal_code"]):
                return jsonify({"details": "Invalid format for postal_code."}), 400
        elif field == "phone":
            if not validate_phone_number(response_body["phone"]):
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
    # TODO: ID VALIDATION DECORATOR
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({"message": f"Customer {customer_id} was not found"}), 404

    response_body = request.get_json()
    #TODO: VALID INPUT DECORATOR FOR PUT/POST
    mandatory_fields = ["name", "postal_code", "phone"]
    for field in mandatory_fields:
        if field not in response_body:
            return jsonify({"details": f"Request body must include {field}."}), 400

    customer.update_from_response(response_body)
    db.session.commit()

    return jsonify(customer.to_dict()), 200

@customers_bp.route("<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    """Deletes customer account by id."""
    # TODO: ID VALIDATION DECORATOR
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({"message": f"Customer {customer_id} was not found"}), 404

    db.session.delete(customer)
    db.session.commit()

    return jsonify({"id": customer.id}), 200