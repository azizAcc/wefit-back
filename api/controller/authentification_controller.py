from flask_restx import Namespace, Resource
from flask import request
from api.service.athentification_service import AuthService
from ..model import Tracker
from ..service.tracking_service import tracking_service

auth_api = Namespace(
    'authentification',
    description='athentification controller')


@auth_api.route('/login', methods=['POST'])
class LoginController(Resource):
    def post(self):
        data = request.get_json()
        print(data)
        user = AuthService.loginService(data['email'], data['password'])
        if user:
            print(user)
            user_json = {key: value for key, value in user.__dict__.items() if key != '_sa_instance_state'}

            print(user_json)
            us = {key: value for key, value in user_json.items() if key != 'password'}
            print(us)
            tracker = Tracker(id_user=us['id'], action='login', description='logged in')
            tracking_service.registerTracking(tracker)
            return us
        return {'code': 404}


@auth_api.route('/register', methods=['POST'])
class RegisterController(Resource):
    def post(self):
        data = request.get_json()
        print(data)
        if AuthService.user_exist(data['email']) is not True:
            user = AuthService.registerService(data)
            if user:
                tracker = Tracker(id_user=user.id, action='register', description='registered in')
                tracking_service.registerTracking(tracker)
                return {'code': 200}

        return {'code': 404}


@auth_api.route('/getusers', methods=['GET'])
class GetUsersController(Resource):
    def get(self):
        try:
            users = AuthService.getAllUsers()
            if users:
                users_json = [{key: value for key, value in item.__dict__.items() if key != '_sa_instance_state'}
                              for item in users]
                return users_json
        except Exception as e:
            raise e
