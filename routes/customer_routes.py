from app import db
from app.models.customer import Customer
from app.models.rental import Rental
from app.models.video import Video
from flask import Blueprint, jsonify,request, make_response, abort 
from datetime import date

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")


# TODO ZIP CODE VALIDATION,
#       PHONE NUM VALIDATION,
def timestamp():
    """
    Determines current time and formats to specficiation.
    e.g. "Wed, 16 Apr 2014 21:40:20 -0700"""
    #TODO: fix datetime formatting
    now = date.today().strftime("%a, %d %b %Y %H:%M:%S %Z")
    return now

@customers_bp.route("", methods=["GET"])
def get_all_customer():
    """Retrieves all customers from database."""
    customers = Customer.query.all()

    return jsonify([customer.to_dict() for customer in customers]), 200

@customers_bp.route("<customer_id>", methods=["GET"])
def get_customer_by_id(customer_id):
    """Retreives customer data by id."""
    # TODO: Refactor 404 for JSON
    customer = Customer.query.get_or_404(customer_id)

    return jsonify(customer.to_dict())

@customers_bp.route("", methods=["POST"])
def create_customer():
    """Creates a customer from JSON user input."""
    response_body = request.get_json()
    print(response_body)

    #TODO: Refactor reused code below
    #TODO: Validate input
    mandatory_fields = ["name", "postal_code", "phone"]
    for field in mandatory_fields:
        if field not in response_body:
            return jsonify(f"{field.capitalize()} missing. Unable to create cusomer account."), 400

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
    customer = Customer.query.get_or_404(customer_id)

    response_body = request.get_json()
    #TODO: Refactor reused code below
    #TODO: Validate input
    mandatory_fields = ["name", "postal_code", "phone"]
    for field in mandatory_fields:
        if field not in response_body:
            return jsonify(f"{field.capitalize()} missing. Unable to update cusomer account."), 400

    customer.update_from_response(response_body)
    db.session.commit()

    return jsonify(customer.to_dict()), 200

@customers_bp.route("<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    """Deletes customer account by id."""
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()

    return jsonify({"id": customer.id}), 200