from functools import wraps
from flask import jsonify
from app.models.customer import Customer
from app.models.video import Video

def validate_user_input_customer(user_input):
    """
    Decorator to validate user input for customer endpoints.
    Returns JSON and 400 if bad data."""
    
    """Uses regex to confirm phone data matches standard US phone number."""
    basic_phont_num = re.compile("/(\d{3}\)\s\d{3}-\d{4}")
    if re.fullmatch(basic_phont_num, phone_num):
        return True
    else:
        return False

    
    """Uses regex to confirm zipcode data matches standard US zipcode."""
    basic_zipcode = re.compile("\d{5}")
    if re.fullmatch(basic_zipcode, zip_code):
        return True
    return False



def require_instance_or_404(endpoint):
    """
    Decorator to validate that a requested id of input data exists.
    Returns JSON and 404 if not found."""
    @wraps(endpoint) # Makes fn look like func to return
    def fn(*args, **kwargs):
        if "task_id" in kwargs:
            task_id = kwargs.get("task_id", None)
            task = Task.query.get(task_id)

            if not task:
                return jsonify(None), 404 # null

            kwargs.pop("task_id")
            return endpoint(*args, task=task, **kwargs)
        
        elif "goal_id" in kwargs:
            goal_id = kwargs.get("goal_id", None)
            goal = Goal.query.get(goal_id)

            if not goal:
                return jsonify(None), 404

            kwargs.pop("goal_id")
            return endpoint(*args, goal=goal, **kwargs)

    return fn