from app import db
from app.models.customer import Customer
from app.models.rental import Rental
from app.models.video import Video
# from app.utils.validation_decorators import validate_kwarg
from flask import Blueprint, jsonify,request, make_response, abort 
from datetime import date, datetime, timezone
import re

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")

def validate_endpoint_id(id):
    """Validates id for endpoint is an integer."""
    try:
        int(id)
    except:
        abort(make_response({f"details": "Endpoint must be an int."}, 400))

def timestamp():
    """
    Determines current time and formats to specficiation.
    e.g. "Wed, 16 Apr 2014 21:40:20 -0700"""
    #TODO: fix datetime formatting
    #TODO: Should this go here? Customer method?
    now = datetime.now(timezone.utc).astimezone().strftime("%a, %d %b %Y %H:%M:%S %z")
    print(now) # Sat, 06 Nov 2021 21:37:21 -0700 (DOESN'T PRINT THIS WAY IN POSTMAN)
    return now

#TODO: SHOULD FLASK METHODS BE COMPLETELY SEPARATE FROM MODELS??
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

def validate_customer_instance(id):
    """
    Function that validates the existence of customer instance, and
    returns instance of customer."""
    # Validates customer instance exists
    customer = Customer.query.get(id)
    if not customer:
        abort(make_response({"message": f"Customer {id} was not found"}, 404))
    return customer

def validate_form_data(form_data):
    """Validates request body."""
    mandatory_fields = ["name", "postal_code", "phone"]
    for field in mandatory_fields:
        if field not in form_data:
            abort(make_response({"details": f"Request body must include {field}."}, 400))
    return True

@customers_bp.route("", methods=["GET"])
def get_all_customer():
    """Retrieves all customers from database."""
    customers = Customer.query.all()
    return jsonify([customer.to_dict() for customer in customers]), 200

@customers_bp.route("<customer_id>", methods=["GET"])
# @validate_kwarg
def get_customer_by_id(customer_id):
    """Retreives customer data by id."""
    validate_endpoint_id(customer_id)
    customer = validate_customer_instance(customer_id)
    return jsonify(customer.to_dict())

@customers_bp.route("", methods=["POST"])
def create_customer():
    """Creates a customer from JSON user input."""
    form_data = request.get_json()
    validate_form_data(form_data)

    if not validate_postal_code(form_data["postal_code"]):
        return jsonify({"details": "Invalid format for postal_code."}), 400
    if not validate_phone_number(form_data["phone"]):
        return jsonify({"details": "Invalid format for phone number."}), 400

    new_customer = Customer(
        name=form_data["name"],
        registered_at=timestamp(),
        postal_code=form_data["postal_code"],
        phone=form_data["phone"]
    )
    db.session.add(new_customer)
    db.session.commit()
    
    return jsonify({"id": new_customer.id}), 201

@customers_bp.route("<customer_id>", methods=["PUT"])
def update_customer_by_id(customer_id):
    """Updates all customer data by id"""
    customer = validate_customer_instance(customer_id)

    form_data = request.get_json()
    validate_form_data(form_data)
    customer.update_from_response(form_data)
    db.session.commit()

    return jsonify(customer.to_dict()), 200

@customers_bp.route("<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    """Deletes customer account by id."""
    validate_endpoint_id(customer_id)
    customer = validate_customer_instance(customer_id)

    db.session.delete(customer)
    db.session.commit()

    return jsonify({"id": customer.id}), 200

@customers_bp.route("<customer_id>/rentals", methods=["GET"])
def get_rentals_by_customer_id(customer_id):
    """Retrieves all rentals associated with specific customer."""
    validate_endpoint_id(customer_id)
    validate_customer_instance(customer_id)

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