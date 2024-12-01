# __init__.py
from flask import Flask, Blueprint
from dotenv import load_dotenv
from flask_cors import CORS
from flask_restx import Api
from api.controller.authentification_controller import auth_api
from api.controller.coach_controller import coach_api
from api.controller.annonce_controller import annonce_api
from api.controller.user_controller import user_api
from api.controller.wait_list_controller import waitlist_api
from api.extensions import db, bcrypt, jwt
from api.model import User, SportIcon, Spatial
from datetime import timedelta

load_dotenv()


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r'/*': {'origins': '*'}})

    app.config['JWT_SECRET_KEY'] = '3a6f3928b08c1fdf2849fe5da9e1d28f829a8729'  # Change this in production
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)  # Access token expiry
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)  # Refresh token expiry
    jwt.init_app(app)

    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://wefit_db_user:aMzmBuCYPIKjqgdD3p3I1xNhJ1fzYgUw@dpg-cq0nrq3v2p9s73cdie40-a.frankfurt-postgres.render.com/wefit_db"
    db.init_app(app)
    bcrypt.init_app(app)
    blueprint = Blueprint('api_bp', __name__)
    api = Api(
        blueprint,
        title="upload api",
        version="1",
        description="Api for uplaod me project")

    # api.add_namespace(bucket_api, "/aws")
    # api.add_namespace(stripe_api, "/stripe")
    api.add_namespace(auth_api, "/auth")
    api.add_namespace(user_api, "/user")
    api.add_namespace(coach_api, "/coach")
    api.add_namespace(annonce_api, "/annonce")
    api.add_namespace(waitlist_api, "/waitlist")
    app.register_blueprint(blueprint, methods=['GET', 'POST', 'PUT', 'DELETE'])

    return app
