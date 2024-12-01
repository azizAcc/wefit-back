from flask_restx import Namespace, Resource
from flask import request, jsonify

from api.service.user_service import UserService
from api.service.authentification_service import AuthService
user_api = Namespace(
    'user controller',
    description='Authentication controller'
)

@user_api.route('/edit/all', methods=['POST'])
class EditInformation(Resource):
    def post(self):
        data = request.get_json()
        print(data)
        try:
            if AuthService.user_exist(data['old_email']):
                if UserService.UpdateInformation(data):
                    return {'code': 200}
        except Exception as e:
            print(e)
            return {'code': 400}
