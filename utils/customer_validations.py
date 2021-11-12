from functools import wraps
from flask import jsonify, make_response, abort
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

def validate_form_data(response_body):
    """Validates request body."""
    mandatory_fields = ["name", "postal_code", "phone"]
    for field in mandatory_fields:
        if field not in response_body:
            abort(make_response({"details": f"Request body must include {field}."}, 400))
    return True

# def require_instance_or_404(endpoint):
#     """
#     Decorator to validate that a requested id of input data exists.
#     Returns JSON and 404 if not found."""
#     @wraps(endpoint) # Makes fn look like func to return
#     def fn(*args, **kwargs):
#         if "task_id" in kwargs:
#             task_id = kwargs.get("task_id", None)
#             task = Task.query.get(task_id)

#             if not task:
#                 return jsonify(None), 404 # null

#             kwargs.pop("task_id")
#             return endpoint(*args, task=task, **kwargs)
        
#         elif "goal_id" in kwargs:
#             goal_id = kwargs.get("goal_id", None)
#             goal = Goal.query.get(goal_id)

#             if not goal:
#                 return jsonify(None), 404

#             kwargs.pop("goal_id")
#             return endpoint(*args, goal=goal, **kwargs)

#     return fn