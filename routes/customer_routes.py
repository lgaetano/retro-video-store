from app import db
from app.models.customer import Customer
from app.models.rental import Rental
from app.models.video import Video
from flask import Blueprint, jsonify,request, make_response, abort 

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")


# TODO ZIP CODE VALIDATION,
#       PHONE NUM VALIDATION,

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

@customers_bp.route("<customer_id>", methods=["PUT"])
def update_customer_by_id(customer_id):
    """Updates all customer data by id"""
    pass
