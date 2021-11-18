from flask import make_response, abort
from app.models.video import Video

def validate_video_instance(video_id):
    """Confirms instances of Video exists."""
    video = Video.query.get(video_id)
    if not video:
        abort(make_response({"message" :f"Video {video_id} was not found"}, 404))
    return video

def validate_request_body(request_body):
    """Validates request body."""
    mandatory_fields = ["title","total_inventory","release_date"]
    for field in mandatory_fields:
        if field not in request_body:
            abort(make_response({"details": f"Request body must include {field}."}, 400))
    return True