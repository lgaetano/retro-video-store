
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
        endpoint_ids = ["customer_id", "video_id"]
        if "customer_id" in endpoint_ids:
            customer_id = kwargs.get("customer_id", None)
            try:
                int(customer_id)
            except:
                abort(make_response({f"details": f"{customer_id} must be an int."}, 400))
            
            kwargs.pop("customer_id")
            return endpoint(*args, customer_id=customer_id, **kwargs)

        elif "video_id" in endpoint_ids:
            video_id = kwargs.get("video_id", None)
            try:
                int(video_id)
            except:
                abort(make_response({f"details": f"{video_id} must be an int."}, 400))
            
            kwargs.pop("video_id")
            return endpoint(*args, video_id=video_id, **kwargs)

    return fn