from app import db
from app.models.customer import Customer
from app.models.rental import Rental
from app.models.video import Video
from flask import Blueprint, jsonify,request, make_response, abort 

videos_bp = Blueprint("videos",__name__,url_prefix="/videos")

def validate_id(id):
    """Validates id for endpoint is an integer."""
    try:
        int(id)
    except:
        # abort(jsonify({f"details": "{param_id} must be an int."}), 400) # TODO: Why didn't this work?
        abort(make_response({f"details": "Endpoint must be an int."}, 400))

@videos_bp.route("", methods=["GET"])
def get_all_videos():
    """Retrieves all videos from database."""
    videos = Video.query.all()

    return jsonify([video.to_dict() for video in videos]), 200

@videos_bp.route("/<video_id>", methods=["GET"])
def get_video_by_id(video_id):
    """Retreives video data by id."""
    validate_id(video_id)
    # TODO: Refactor 404 for JSON
    video = Video.query.get(video_id)

    if not video:
        return jsonify({"message":f"Video {video_id} was not found"}), 404

    return jsonify(video.to_dict()), 200

@videos_bp.route("", methods=["POST"])
def create_video():
    """Creates instance of customer from user input."""
    response_body = request.get_json()

    # TODO: Valid input decorator for PUT/POST
    mandatory_fields = ["title", "total_inventory", "release_date"]
    for field in mandatory_fields:
        if field not in response_body:
            return jsonify({"details": f"Request body must include {field}."}), 400
        # TODO: Add regex validation for releast date and int verification for totla_inventory

    new_video = Video(
        title=response_body["title"],
        total_inventory=response_body["total_inventory"],
        release_date=response_body["release_date"]
    )
    db.session.add(new_video)
    db.session.commit()

    return jsonify({"id": new_video.id}), 201

@videos_bp.route("/<video_id>", methods=["PUT"])
def update_video(video_id):
    """Updates video from user data."""
    validate_id(video_id)
    video = Video.query.get(video_id)
    if not video:
        return jsonify({"message": f"Video {video_id} was not found"}), 404
    
    # TODO: Valid input decorator for PUT/POST
    response_body = request.get_json()
    mandatory_fields = ["title", "release_date", "total_inventory"]
    for field in mandatory_fields:
        if field not in response_body:
            return jsonify({"details": f"Request body must include {field}."}), 400
        # TODO: Add regex validation for releast date and int verification for totla_inventory

    video.updates_from_dict(response_body)
    db.session.commit()
    return jsonify(video.to_dict()), 200

@videos_bp.route("/<video_id>", methods=["DELETE"])
def delete_video(video_id):
    """Deletes video data by id."""
    validate_id(video_id)
    video = Video.query.get(video_id)
    if not video:
        return jsonify({"message": f"Video {video_id} was not found"}), 404
    
    db.session.delete(video)
    db.session.commit()
    return jsonify({"id": video.id}), 200