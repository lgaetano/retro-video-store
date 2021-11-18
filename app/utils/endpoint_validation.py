
from functools import wraps
from flask import make_response, abort
from app.models.customer import Customer
from app.models.video import Video

def validate_endpoint(endpoint):
    """Decorator to validate that endpoint id is an int. Returns JSON and 
    400 if not found.
    """
    @wraps(endpoint) # Makes fn look like func to return
    def fn(*args, **kwargs):
        """Validates id for endpoint is an integer."""
        if "customer_id" in kwargs:
            customer_id = kwargs.get("customer_id", None)
            try:
                int(customer_id)
            except:
                abort(make_response({f"details": f"{customer_id} must be an int."}, 400))
            
            customer = Customer.query.get(customer_id)
            if not customer:
                abort(make_response({"message" :f"Customer {customer_id} was not found"}, 404))

            kwargs.pop("customer_id")
            return endpoint(*args, customer=customer, **kwargs)

        elif "video_id" in kwargs:
            video_id = kwargs.get("video_id", None)
            try:
                int(video_id)
            except:
                abort(make_response({f"details": f"{video_id} must be an int."}, 400))

            video = Video.query.get(video_id)
            if not video:
                abort(make_response({"message" :f"Video {video_id} was not found"}, 404))
            
            kwargs.pop("video_id")
            return endpoint(*args, video=video, **kwargs)

    return fn