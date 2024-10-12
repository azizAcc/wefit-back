# __init__.py


from flask import Flask, Blueprint
from dotenv import load_dotenv
from flask_cors import CORS
from flask_restx import Api
# from api.controller.aws_controller import bucket_api
# from api.controller.stripe_controller import stripe_api
from api.controller.authentification_controller import auth_api
from api.extensions import db, bcrypt
from api.model import User, Coach, SportIcon


load_dotenv()


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r'/*': {'origins': '*'}})
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
    app.register_blueprint(blueprint, methods=['GET', 'POST'])

    return app
