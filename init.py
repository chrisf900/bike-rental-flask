import os

from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate

from createdata import bp
from database import db

load_dotenv(".env")

migrate = Migrate()


def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

    db.init_app(app=app)
    migrate.init_app(app=app, db=db)
    app.register_blueprint(bp)

    return app
