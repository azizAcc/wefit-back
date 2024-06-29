# __init__.py


from flask import Flask, Blueprint
from dotenv import load_dotenv
from flask_cors import CORS
from flask_restx import Api
from api.controller.aws_controller import bucket_api
from api.controller.stripe_controller import stripe_api
from api.controller.authentification_controller import auth_api
from api.controller.tracking_controller import api_tracker
from api.controller.contact_controller import contact_api
from api.extensions import db, bcrypt
from api.model import User, Tracker, Payments, Files, Links


load_dotenv()


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r'/*': {'origins': '*'}})
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://upload_file_user:zW1fgnkC9KVXgPh4F9vf4zfwPNdotVd6@dpg-coi0s7ol5elc73cvt1sg-a.frankfurt-postgres.render.com/upload_file"
    db.init_app(app)
    bcrypt.init_app(app)
    blueprint = Blueprint('api_bp', __name__)
    api = Api(
        blueprint,
        title="upload api",
        version="1",
        description="Api for uplaod me project")

    api.add_namespace(bucket_api, "/aws")
    api.add_namespace(stripe_api, "/stripe")
    api.add_namespace(auth_api, "/auth")
    api.add_namespace(api_tracker, "/tracker")
    api.add_namespace(contact_api, "/contact")
    app.register_blueprint(blueprint, methods=['GET', 'POST'])

    return app
