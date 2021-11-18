from app import db
from flask import Blueprint, jsonify,request, make_response, abort 
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from app.utils.endpoint_validation import validate_endpoint
from app.utils.video_validation import validate_video_instance, validate_request_body
from sqlalchemy import func

bp = Blueprint("videos",__name__,url_prefix="/videos")

def query_params():
    """Assembles query based off query parameters: 
    
    'sort' : sort data by 'name', 'registered_at', and 'postal_code'
    'n' : items per page
    'p' : page number.
    
    Function returns assembled query and 'True' if return objects is a
    Pagination object, 'False' if a list.
    """
    query = Customer.query

    # Accepted query params
    sort = request.args.get("sort")
    n = request.args.get("n")
    p = request.args.get("p")

    if sort == "title":
        query = query.order_by(func.lower(Video.title))
    elif sort == "date":
        query = query.order_by(Video.date.desc())

    try:
        if n and p:
            query = query.paginate(page=int(p), per_page=int(n))          
        elif p:
            query = query.paginate(page=int(p))
        elif n:
            query = query.paginate(per_page=int(n))
        else:
            query = query.all() # Final query, not paginated
            return query, False
    except:
        abort(make_response({"details":"Page not found."},404))

    # Final query, paginated
    return query, True

@bp.route("", methods=["GET"])
def get_all_videos():
    """Retrieves all videos from database."""
    query, paginated = query_params()
    if paginated:
        # If query is Pagination obj, requires .items
        return jsonify([video.to_dict() for video in query.items]), 200
    return jsonify([video.to_dict() for video in query]), 200

@bp.route("/<video_id>",methods=["GET"])
@validate_endpoint
def get_video_by_id(video):
    """Retreives video data by id."""
    return jsonify(video.to_dict()), 200
    
@bp.route("", methods=["POST"])
def create_video():
    """Creates a video from JSON user input."""
    request_body = request.get_json()
    validate_request_body(request_body)

    new_video = Video(
        title=request_body["title"],
        total_inventory=request_body["total_inventory"],
        release_date=request_body["release_date"]
        )
    db.session.add(new_video)
    db.session.commit()
    return jsonify(new_video.to_dict()), 201      

@bp.route("/<video_id>", methods=["PUT"])
@validate_endpoint
def update_video_by_id(video):
    """Updates all video data by id."""
    request_body = request.get_json()
    validate_request_body(request_body)

    video.update_from_response(request_body)
    db.session.commit() 
    return jsonify(video.to_dict()), 200

@bp.route("/<video_id>", methods=["DELETE"])
@validate_endpoint
def delete_video_by_id(video):
    """Deletes video account by id."""
    db.session.delete(video)
    db.session.commit()
    return jsonify(video.to_dict()), 200

@bp.route("<video_id>/rentals", methods=["GET"])
@validate_endpoint
def get_rentals_by_video_id(video):
    """Retrieves all rentals associated with a specific video."""
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

@bp.route("<video_id>", methods=["GET"])
@validate_endpoint
def get_video_rental_history(video):
    """For a specific video, returns list of all customers that 
    have checked out in the past.
    """
    results = db.session.query(Rental, Video, Customer) \
                        .select_from(Rental).join(Video).join(Customer).all()
    response = []
    for rental, video, customer, in results:
        response.append({
            "id":customer.id,
            "name":customer.name,
            "postal_code":customer.postal_code,
            "checkout_date":customer.registered_at,
            "due_date":rental.due_date,
        })
    return jsonify(response), 200
