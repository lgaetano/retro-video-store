from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import click
from dotenv import load_dotenv
# from .seed.customer_data import seed

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ECHO"] = True

    if test_config is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_DATABASE_URI")
    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_TEST_DATABASE_URI")

    # Setup DB
    db.init_app(app)
    migrate.init_app(app, db)

    # import models for Alembic Setup and register Blueprints
    from .routes import customer, video, rental
    app.register_blueprint(customer.bp)
    app.register_blueprint(rental.bp)
    app.register_blueprint(video.bp)

    # @click.add_command('db_seed')
    # def db_seed():
    #     """Seeds db using CLI and Faker generator."""
    #     seed()

    return app