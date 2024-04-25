import os

from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from createdata import create_data_bp
from database import db
from users.api.resources.auth import auth_bp
from users.api.resources.profile import profile_bp
from users.lib.constants import ACCESS_EXPIRES

load_dotenv(".env")

migrate = Migrate()


def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

    db.init_app(app=app)
    migrate.init_app(app=app, db=db)
    add_extensions(app)

    return app


def add_extensions(app):
    app.register_blueprint(create_data_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(auth_bp)

    app.config["JWT_SECRET_KEY"] = os.environ["FLASK_JWT_SECRET_KEY"]
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
    app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
    app.config["JWT_HEADER_NAME"] = "Authorization"
    app.config["JWT_HEADER_TYPE"] = "Bearer"
    JWTManager(app)
