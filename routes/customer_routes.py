from app import db
from flask import Blueprint, jsonify,request, make_response, abort
from sqlalchemy import func
from app.models.customer import Customer
from app.models.rental import Rental
from app.models.video import Video
from utils.customer_validations import validate_request_body, validate_customer_instance,\
        validate_postal_code, validate_phone_number
from utils.endpoint_validation import validate_endpoint_is_int
from datetime import date, datetime, timezone

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")

def timestamp():
    """
    Determines current time and formats to specficiation.
    e.g. "Wed, 16 Apr 2014 21:40:20 -0700"""
    now = datetime.now(timezone.utc).astimezone() #.strftime("%a, %d %b %Y %H:%M:%S %z")
    return now

def query_params():
    """Assembles query based off query parameters: 
    
    'sort' : sort data by 'name', 'registered_at', and 'postal_code'
    'n' : items per page
    'p' : page number.
    
    Function returns assembled query and 'True' if return objects is a
    Pagination object, 'False' if a list.
    """
    query = Customer.query
    # Accepted query params
    sort = request.args.get("sort")
    n = request.args.get("n")
    p = request.args.get("p")

    if sort == "name":
        query = query.order_by(func.lower(Customer.name))
    elif sort == "registered_at":
        query = query.order_by(Customer.registered_at.desc())
    elif sort == "postal_code":
        query = query.order_by(Customer.postal_code)

    try:
        if n and p:
            query = query.paginate(page=int(p), per_page=int(n))          
        elif p:
            query = query.paginate(page=int(p))
        elif n:
            query = query.paginate(per_page=int(n))
        else:
            query = query.all() # Final query, not paginated
            return query, False
    except:
        abort(make_response({"details":"Page not found."},404))

    # Final query, paginated
    return query, True

@customers_bp.route("", methods=["GET"])
def get_all_customers():
    """Retrieves all customers from database."""
    query, paginated = query_params()
    if paginated:
        # If query is Pagination obj, requires .items
        return jsonify([customer.to_dict() for customer in query.items]), 200
    return jsonify([customer.to_dict() for customer in query]), 200


@customers_bp.route("/<customer_id>", methods=["GET"])
@validate_endpoint_is_int
def get_customer_by_id(customer_id):
    """Retreives customer data by id."""
    customer = validate_customer_instance(customer_id)
    return jsonify(customer.to_dict())

@customers_bp.route("", methods=["POST"])
def create_customer():
    """Creates a customer from JSON user input."""
    request_body = request.get_json()
    validate_request_body(request_body)

    if not validate_postal_code(request_body["postal_code"]):
        return jsonify({"details": "Invalid format for postal_code."}), 400
    if not validate_phone_number(request_body["phone"]):
        return jsonify({"details": "Invalid format for phone number."}), 400

    new_customer = Customer(
        name=request_body["name"],
        registered_at=timestamp(),
        postal_code=request_body["postal_code"],
        phone=request_body["phone"]
    )

    db.session.add(new_customer)
    db.session.commit()
    return jsonify({"id": new_customer.id}), 201

@customers_bp.route("<customer_id>", methods=["PUT"])
@validate_endpoint_is_int
def update_customer_by_id(customer_id):
    """Updates all customer data by id"""
    customer = validate_customer_instance(customer_id)

    request_body = request.get_json()
    validate_request_body(request_body)

    customer.update_from_response(request_body)
    db.session.commit()

    return jsonify(customer.to_dict()), 200

@customers_bp.route("<customer_id>", methods=["DELETE"])
@validate_endpoint_is_int
def delete_customer(customer_id):
    """Deletes customer account by id."""
    customer = validate_customer_instance(customer_id)
    db.session.delete(customer)
    db.session.commit()

    return jsonify({"id": customer.id}), 200


@customers_bp.route("<customer_id>/rentals", methods=["GET"])
@validate_endpoint_is_int
def get_rentals_by_customer_id(customer_id):
    """Returns list of videos currently assigned to customer."""
    validate_customer_instance(customer_id)

    rentals = db.session.query(Rental, Customer, Video) \
                        .select_from(Rental).join(Customer).join(Video).all()
    
    response = []
    for rental, customer, video in rentals:
        response.append({
            "release_date": video.release_date,
            "title": video.title,
            "due_date": rental.calculate_due_date(),
    })
        
    return jsonify(response), 200

@customers_bp.route("/<customer_id>/history", methods=["GET"])
@validate_endpoint_is_int
def get_customer_rental_history(customer_id):
    """Returns list of all videos a customer has checked out in the past"""
    validate_customer_instance(customer_id)

    rentals = db.session.query(Rental, Customer, Video) \
                        .select_from(Rental).join(Customer).join(Video).all()

    response = []
    for rental, customer, video in rentals:
        response.append({
            "title": video.title,
            "checkout_date": rental.calculate_checkout_date(),
            "due_date": rental.calculate_due_date()
        })

    return jsonify(response), 200