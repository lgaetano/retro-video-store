from app import db
from app.models.customer import Customer
from app.models.rental import Rental
from app.models.video import Video
from flask import Blueprint, jsonify,request, make_response, abort 
from app.utils.endpoint_validation import validate_endpoint
from app.utils.video_validation import validate_video_instance, validate_request_body
from sqlalchemy import func

bp = Blueprint("videos",__name__,url_prefix="/videos")

@bp.route("", methods=["GET"])
def get_all_videos():
    """"""
    query_param = [key for key in request.args.keys()]
    page = request.args.get("page", 1, type=int)
    ROWS_PER_PAGE = 3
    if  query_param == []:
        videos = Video.query.order_by(Video.id.asc())
    elif "page" in query_param and "sort" in query_param and request.args.get("sort") == "title":
        try:
            videos = Video.query.order_by(func.lower(Video.title)).paginate(page=page, per_page=ROWS_PER_PAGE)
            videos = videos.items
        except:
            abort(make_response({"details":"Page not found."},404))
    elif "sort" in query_param and request.args.get("sort") == "title":
        videos = Video.query.order_by(func.lower(Video.title))
    elif "sort" in query_param and request.args.get("sort") == "date":
        videos = Video.query.order_by(Video.release_date)
    elif "page" in query_param:
        try:
            videos = Video.query.order_by(Video.id).paginate(page=page, per_page=ROWS_PER_PAGE)
            videos = videos.items
        except:
            abort(make_response({"details":"Page out of range."},400))
    response_body = [video.video_dict() for video in videos]
    return jsonify(response_body),200  

@bp.route("/<video_id>",methods=["GET"])
@validate_endpoint
def get_video_by_id(video_id):
    """Retreives video data by id."""
    video = validate_video_instance(video_id)
    return jsonify(video.video_dict()), 200
    
@bp.route("", methods=["POST"])
def create_video():
    """Creates a customer from JSON user input."""
    request_body = request.get_json()
    validate_request_body(request_body)

    new_video = Video(
        title=request_body["title"],
        total_inventory=request_body["total_inventory"],
        release_date=request_body["release_date"]
        )
    db.session.add(new_video)
    db.session.commit()
    return jsonify({"id": new_video.id}), 201      

@bp.route("/<video_id>", methods=["PUT"])
@validate_endpoint
def update_video_by_id(video_id):
    """Updates all video data by id"""
    video = validate_video_instance(video_id)
    
    request_body = request.get_json()
    validate_request_body(request_body)

    video.update_from_response(request_body)
    db.session.commit() 
    return jsonify(video.to_dict()), 200

@bp.route("/<video_id>", methods=["DELETE"])
@validate_endpoint
def delete_video_by_id(video_id):
    """Deletes video account by id."""
    video = validate_video_instance(video_id)
    db.session.delete(video)
    db.session.commit()
    return jsonify(video.video_dict()), 200

@bp.route("<video_id>/rentals", methods=["GET"])
@validate_endpoint
def get_rentals_by_video_id(video_id):
    """Retrieves all rentals associated with a specific video."""
    video = validate_video_instance(video_id)
    results = db.session.query(Rental,Video, Customer ) \
                        .select_from(Rental).join(Video).join(Customer).all()
    response = []
    for rental,video, customer,  in results:
        response.append({
            "due_date":rental.calculate_due_date(),
            "name":customer.name,
            "phone":customer.phone,
            "postal_code":customer.postal_code
        })
    return jsonify(response),200

@bp.route("<video_id>", methods=["get"])
@validate_endpoint
def video_customer_rental_history(video_id):
    """"""
    video = validate_video_instance(video_id)
    results = db.session.query(Rental,Video, Customer ) \
                        .select_from(Rental).join(Video).join(Customer).all()
    response = []
    for rental,video, customer,  in results:
        response.append({
            "id":customer.id,
            "name":customer.name,
            "postal_code":customer.postal_code,
            "checkout_date":customer.registered_at,
            "due_date":rental.due_date,
        })
    return jsonify(response),200
