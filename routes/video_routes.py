from app import db
from app.models.customer import Customer
from app.models.rental import Rental
from app.models.video import Video
from flask import Blueprint, jsonify,request, make_response, abort 
from sqlalchemy import func

customers_bp = Blueprint("customers", __name__,url_prefix="/customers")
rentals_bp = Blueprint("rentals",__name__,url_prefix="/rentals")
videos_bp = Blueprint("videos",__name__,url_prefix="/videos")

# helper function
def valid_int(number,parameter_type):
    try:
        int(number)
    except:
        abort(make_response({"error":f"{parameter_type} must be an int"},400))
def validate_video_existence(video_id):
    video = Video.query.get(video_id)
    if not video:
        abort(make_response({"message":f"Video {video_id} was not found"},404))
    return video
def validate_request_body(request_body):
    video_keys = ["title","total_inventory","release_date"]
    for key in video_keys:
        if key not in request_body:
            abort(make_response({"details":f'Request body must include {key}.'},400))
    
@videos_bp.route("",methods=["GET"])
def get_videos_apply_query_params():
    query_param = [key for key in request.args.keys()]
    page = request.args.get("page",1,type=int)
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

@videos_bp.route("/<video_id>",methods=["GET","DELETE","PUT"])
def handle_video(video_id):
    valid_int(video_id,"video_id")
    video =validate_video_existence(video_id)
    if request.method == "GET":
        return jsonify(video.video_dict()),200
    elif request.method == "DELETE":
        db.session.delete(video)
        db.session.commit()
        return jsonify(video.video_dict()),200
    elif request.method == "PUT":
        request_body = request.get_json()
        validate_request_body(request_body)
        video.title = request_body["title"]
        video.total_inventory = request_body["total_inventory"]
        video.release_date = request_body["release_date"]
        db.session.commit() 
        return jsonify(video.video_dict()),200
    
@videos_bp.route("",methods=["POST"])
def create_video():
    request_body = request.get_json()
    validate_request_body(request_body)
    new_video = Video(
        title = request_body["title"],
        total_inventory = request_body["total_inventory"],
        release_date = request_body["release_date"]
        )
    db.session.add(new_video)
    db.session.commit()
    return jsonify(new_video.video_dict()),201      
    
@videos_bp.route("<video_id>/rentals", methods=["GET"])
def get_rentals_by_video_id(video_id):
    """Retrieves all rentals associated with a specific video."""
    valid_int(video_id, "video_id")
    video = validate_video_existence(video_id)
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

@videos_bp.route("<video_id>",methods=["get"])
def video_customer_rental_history(video_id):
    valid_int(video_id, "video_id")
    video = validate_video_existence(video_id)
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
    


