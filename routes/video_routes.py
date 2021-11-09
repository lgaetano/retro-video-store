from app import db
from app.models.customer import Customer
from app.models.rental import Rental
from app.models.video import Video
from flask import Blueprint, jsonify,request, make_response, abort 

rentals_bp = Blueprint("rentals",__name__,url_prefix="/rentals")
videos_bp = Blueprint("videos",__name__,url_prefix="/videos")

def validate_id(id, param_id):
    """Validates id for endpoint is an integer."""
    try:
        int(id)
    except:
        # abort(jsonify({f"details": "{param_id} must be an int."}), 400) # TODO: Why didn't this work?
        abort(make_response({f"details": "{param_id} must be an int."}, 400))

@videos_bp.route("", methods=["GET"])
def get_all_videos():
    """Retrieves all videos from database."""
    videos = Video.query.all()

    return jsonify([videos.to_dict() for video in videos]), 200

@videos_bp.route("<video_id>", methods=["GET"])
def get_video_by_id(customer_id):
    """Retreives customer data by id."""
    # TODO: Refactor 404 for JSON
    video = Video.query.get_or_404(customer_id)

    return jsonify(video.to_dict())


POST /videos
PUT /videos/<id>
DELETE /videos/<id>