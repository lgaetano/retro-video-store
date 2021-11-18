from flask import make_response, abort
from app.models.customer import Customer
import re

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

def validate_customer_instance(customer_id):
    """Confirms instances of customer exists."""
    customer = Customer.query.get(customer_id)
    if not customer:
        abort(make_response({"message" :f"Customer {customer_id} was not found"}, 404))
    return customer

def validate_request_body(request_body):
    """Validates request body."""
    mandatory_fields = ["name", "postal_code", "phone"]
    for field in mandatory_fields:
        if field not in request_body:
            abort(make_response({"details": f"Request body must include {field}."}, 400))
    return True