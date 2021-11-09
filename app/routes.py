from app import db
from app.models.customer import Customer
from app.models.rental import Rental
from app.models.video import Video
from flask import Blueprint, jsonify,request, make_response, abort 

customers_bp = Blueprint("customers", __name__,url_prefix="/customers")
rentals_bp = Blueprint("rentals",__name__,url_prefix="/rentals")
videos_bp = Blueprint("videos",__name__,url_prefix="/videos")
