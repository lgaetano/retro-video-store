from app import db
from app.models.customer import Customer
from app.models.rental import Rental
from app.models.video import Video
from flask import Blueprint, jsonify,request, make_response, abort 

customers_bp = Blueprint("customers", __name__,url_prefix="/customers")

@customers_bp.route("", methods=["GET"])
def get_all_customer():
    """Retrieves all customers from database."""
    customers = Customer.query.all()

    customer_response = []
    for customer in customers:
        customer_response.append(customer.to_dict())

    return jsonify(customer_response), 200
