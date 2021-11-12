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
    
def validate_video_instance(id):
    """
    Function that validates the existence of video instance."""
    # Validates video instance exists
    video = Video.query.get(id)
    if not video:
        abort(make_response({"message": f"Video {id} was not found"}, 404))
    return video

def validate_form_data(form_data):
    mandatory_fields = ["title", "release_date", "total_inventory"]
    for field in mandatory_fields:
        if field not in form_data:
            abort(make_response({"details": f"Request body must include {field}."}, 400))

@videos_bp.route("", methods=["GET"])
def get_all_videos():
    """Retrieves all videos from database."""
    videos = Video.query.all()

    return jsonify([video.to_dict() for video in videos]), 200

@videos_bp.route("/<video_id>", methods=["GET"])
def get_video_by_id(video_id):
    """Retreives video data by id."""
    validate_endpoint_id(video_id)
    video = validate_video_instance(video_id)
    return jsonify(video.to_dict()), 200

@videos_bp.route("", methods=["POST"])
def create_video():
    """Creates instance of customer from user input."""
    form_data = request.get_json()
    validate_form_data(form_data)
    # TODO: Add regex validation for releast date and int verification for totla_inventory

    new_video = Video(
        title=form_data["title"],
        total_inventory=form_data["total_inventory"],
        release_date=form_data["release_date"]
    )
    db.session.add(new_video)
    db.session.commit()
    
    return jsonify(new_video.to_dict()), 201

@videos_bp.route("/<video_id>", methods=["PUT"])
def update_video(video_id):
    """Updates video from user data."""
    validate_endpoint_id(video_id)

    form_data = request.get_json()
    validate_form_data(form_data)
    # TODO: Add regex validation for releast date and int verification for totla_inventory
        
    video = validate_video_instance(video_id)
    video.updates_from_dict(form_data)
    db.session.commit()
    return jsonify(video.to_dict()), 200

@videos_bp.route("/<video_id>", methods=["DELETE"])
def delete_video(video_id):
    """Deletes video data by id."""
    validate_endpoint_id(video_id)
    video = validate_video_instance(video_id)
    
    db.session.delete(video)
    db.session.commit()
    return jsonify({"id": video.id}), 200

@videos_bp.route("<videos_id>/rentals", methods=["GET"])
def get_rentals_by_customer_id(videos_id):
    """Retrieves all rentals associated with specific customer."""
    validate_endpoint_id(videos_id)
    validate_video_instance(videos_id)

    results = db.session.query(Rental, Video, Customer) \
                        .select_from(Rental).join(Video).join(Customer).all()
    
    response = []
    for rental, video, customer in results:
        response.append({
            "due_date": rental.due_date,
            "name": customer.name,
            "phone": customer.phone,
            "postal_code": customer.postal_code
    })
        
    return jsonify(response), 200