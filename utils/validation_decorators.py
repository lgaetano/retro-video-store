from functools import wraps
from flask import jsonify, make_response, abort
from app.models.customer import Customer
from app.models.video import Video


def validate_endpoint_id_is_int(id):
    """Validates id for endpoint is an integer."""
    try:
        int(id)
    except:
        abort(make_response({f"details": "Endpoint must be an int."}, 400))

def validate_kwarg(endpoint):
    """
    Decorator to validate that a requested id of input data is and int 
    and that the isntance exists. Returns JSON and 404 if not found."""
    @wraps(endpoint) # Makes fn look like func to return
    def fn(*args, **kwargs):
        if "video_id" in kwargs:
            video_id = kwargs.get("video_id", None)
            validate_endpoint_id_is_int(video_id)

            video = Video.query.get(video_id)
            if not video:
                return jsonify(None), 404 # null

            kwargs.pop("video_id")
            return endpoint(*args, video=video, **kwargs)
        
        elif "customer_id" in kwargs:
            customer_id = kwargs.get("customer_id", None)
            validate_endpoint_id_is_int(customer_id)

            customer = Customer.query.get(customer_id)
            if not customer:
                return jsonify(None), 404

            kwargs.pop("customer_id")
            return endpoint(*args, customer=customer, **kwargs)

    return fn