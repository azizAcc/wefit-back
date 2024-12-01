from flask_restx import Namespace, Resource
from flask import request, jsonify
from geoalchemy2 import WKBElement
import ast

from api.model import Annonce, Coach
from api.service.authentification_service import AuthService
from api.service.coach_service import CoachService

annonce_api = Namespace(
    'annonce controller',
    description='Annonce controller'
)


@annonce_api.route('/create', methods=['POST'])
class CreateAnnonce(Resource):
    def post(self):
        try:
            if request.method == 'POST':
                data = request.get_json()
                print(data['sports'])
                CoachService.CreateAnnonce(data)
                print(data)
                return {'status': 200}
        except Exception as e:
            print(e)
            raise e


@annonce_api.route('/get/<id>', methods=['GET'])
class GetAllAnnonces(Resource):
    def get(self, id):
        try:
            annonces = CoachService.GetAllAnnoncesOfSingleCoach(id)
            print(annonces)
            if annonces:
                annonce_json = [
                    {
                        key: value for key, value in annonce.__dict__.items()
                        if key != '_sa_instance_state' and key != 'geomcol'
                    }
                    for annonce in annonces]

                print(annonce_json)
                for annonce in annonce_json:
                    annonce['sport'] = ast.literal_eval(annonce['sport'])

                return {'status': 200, 'annonces': annonce_json}
            return {'status': 400}
        except Exception as e:
            print(e)
            raise e


@annonce_api.route('/delete/<id>', methods=['DELETE'])
class DeleteAnnonce(Resource):
    def delete(self, id):
        try:
            if request.method == 'DELETE':
                CoachService.DeleteAnnonce(id)
                return {'status': 200}
        except Exception as e:
            print(e)
            raise e


@annonce_api.route('/update/<id>', methods=['PUT'])
@annonce_api.param('id', 'Annonce')
class UpdateAnnonce(Resource):
    def put(self, id=None):
        try:
            if request.method == 'PUT' and id:
                data = request.get_json()
                print(f"data : {data}")
                update_annonce = CoachService.UpdateAnnonce(id, data)
                if update_annonce:
                    return {'status': 200}
        except Exception as e:
            print(e)
            raise e
