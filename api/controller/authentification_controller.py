from flask_restx import Namespace, Resource
from flask import request, jsonify
from api.service.authentification_service import AuthService
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required,
    JWTManager, get_jwt_identity
)
from jwt.exceptions import DecodeError, ExpiredSignatureError
from functools import wraps

auth_api = Namespace(
    'authentification',
    description='Authentication controller'
)


# Middleware to check Bearer token presence and format
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"msg": "Token missing or incorrectly formatted"}), 401
            return jsonify({"msg": "Token missing or incorrectly formatted"}), 401

        token = auth_header.split(" ")[1]
        if not token:
            return jsonify({"msg": "Token is null"}), 401

        return f(*args, **kwargs)

    return decorated


# Login Controller
@auth_api.route('/login', methods=['POST'])
class LoginController(Resource):
    def post(self):
        email = request.json.get("email", None)
        password = request.json.get("password", None)
        user = AuthService.loginService(email, password)
        if user:
            user_json = {key: value for key, value in user.__dict__.items() if key != '_sa_instance_state'}
            access_token = create_access_token(identity=user_json)
            refresh_token = create_refresh_token(identity=user_json)
            return jsonify(access_token=access_token, refresh_token=refresh_token)
        return {"msg": "Invalid credentials"}, 401


# Refresh Token Controller
@auth_api.route('/refresh', methods=['POST'])
class RefreshController(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        if current_user:
            new_access_token = create_access_token(identity=current_user)
            return jsonify(access_token=new_access_token)
        return {"msg": "Invalid credentials"}, 401


# Protected Route Controller
@auth_api.route('/protected', methods=['GET'])
class ProtectedController(Resource):
    @token_required
    @jwt_required()
    def get(self):
        try:
            current_user = get_jwt_identity()
            print(current_user)
            if current_user:
                if AuthService.user_exist(current_user['email']):
                    print(current_user)
                    return current_user, 200
                return {"msg": "User does not exist"}, 500
        except ExpiredSignatureError:
            return {"msg": "Token has expired"}, 401
        except DecodeError:
            return {"msg": "Token is malformed"}, 401
        except Exception as e:
            print(e)
            return {"msg": "An unexpected error occurred"}, 500


# Register Controller
@auth_api.route('/register', methods=['POST'])
class RegisterController(Resource):
    def post(self):
        data = request.get_json()
        if not AuthService.user_exist(data['email']):
            user = AuthService.registerService(data)
            if user:
                return {'code': 200}
        return {'code': 404}


@auth_api.route('/name', methods=['POST'])
class RegisterName(Resource):
    def post(self):
        data = request.get_json()
        print(data)
        if AuthService.user_exist(data['email']):
            if AuthService.registerName(data):
                return {'code': 200}


@auth_api.route('/relogin', methods=['POST'])
class NoPasswordLogin(Resource):
    def post(self):
        data = request.get_json()
        user = AuthService.NoPasswordLoginService(data['email'])
        if user:
            user_json = {key: value for key, value in user.__dict__.items() if key != '_sa_instance_state'}
            access_token = create_access_token(identity=user_json)
            refresh_token = create_refresh_token(identity=user_json)
            return jsonify(access_token=access_token, refresh_token=refresh_token)
        return {"msg": "Invalid credentials"}, 401

