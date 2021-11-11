from app import db
from app.models.customer import Customer
from app.models.rental import Rental
from app.models.video import Video
from flask import Blueprint, jsonify,request, make_response, abort 

videos_bp = Blueprint("videos",__name__,url_prefix="/videos")

def validate_endpoint_id(id):
    """Validates id for endpoint is an integer."""
    try:
        int(id)
    except:
        abort(make_response({f"details": "Endpoint must be an int."}, 400))
    
def video_instance_validate(id):
    """
    Function that validates the existence of video instance."""
    # Validates video instance exists
    video = Video.query.get(id)
    if not video:
        abort(make_response({"message": f"Video {id} was not found"}, 404))
    return video

@videos_bp.route("", methods=["GET"])
def get_all_videos():
    """Retrieves all videos from database."""
    videos = Video.query.all()

    return jsonify([video.to_dict() for video in videos]), 200

@videos_bp.route("/<video_id>", methods=["GET"])
def get_video_by_id(video_id):
    """Retreives video data by id."""
    validate_endpoint_id(video_id)
    video = video_instance_validate(video_id)
    return jsonify(video.to_dict()), 200

@videos_bp.route("", methods=["POST"])
def create_video():
    """Creates instance of customer from user input."""
    form_data = request.get_json()

    # TODO: Valid input decorator for PUT/POST
    mandatory_fields = ["title", "release_date", "total_inventory"]
    for field in mandatory_fields:
        if field not in form_data:
            return jsonify({"details": f"Request body must include {field}."}), 400
        # TODO: Add regex validation for releast date and int verification for totla_inventory

    new_video = Video(
        title=form_data["title"],
        total_inventory=form_data["total_inventory"],
        release_date=form_data["release_date"]
    )
    db.session.add(new_video)
    db.session.commit()
    
    return jsonify({"id": new_video.id}), 201

@videos_bp.route("/<video_id>", methods=["PUT"])
def update_video(video_id):
    """Updates video from user data."""
    validate_endpoint_id(video_id)
    # TODO: Valid input decorator for PUT/POST
    form_data = request.get_json()

    mandatory_fields = ["title", "release_date", "total_inventory"]
    for field in mandatory_fields:
        if field not in form_data:
            return jsonify({"details": f"Request body must include {field}."}), 400
        # TODO: Add regex validation for releast date and int verification for totla_inventory
        
    video = video_instance_validate(video_id)

    video.updates_from_dict(form_data)
    db.session.commit()
    return jsonify(video.to_dict()), 200

@videos_bp.route("/<video_id>", methods=["DELETE"])
def delete_video(video_id):
    """Deletes video data by id."""
    validate_endpoint_id(video_id)
    video = video_instance_validate(video_id)
    
    db.session.delete(video)
    db.session.commit()
    return jsonify({"id": video.id}), 200