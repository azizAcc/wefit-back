import ast

from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required,
    JWTManager, get_jwt_identity
)
from flask_restx import Namespace, Resource
from flask import request, jsonify

from api.model import Coach
from api.service.authentification_service import AuthService
from api.service.coach_service import CoachService

coach_api = Namespace(
    'coach controller',
    description='Coach controller'
)


@coach_api.route('/<id>')
class GetSingleCoachData(Resource):
    def get(self, id=None):
        try:
            if request.method == 'GET' and id is not None:
                coach = CoachService.getSingleCoach(id)
                print(coach)
                if coach:
                    coach_json = {key: value for key, value in coach.__dict__.items() if
                                  key != '_sa_instance_state' and key != 'geomcol'}
                    print(coach_json)
                    crypted_coach = create_access_token(identity=coach_json)
                    print(crypted_coach)
                    return jsonify(crypted_coach=crypted_coach, status=200)
                return {'status': 400}
        except Exception as e:
            print(e)
            return {'status': 400, 'message': str(e)}


@coach_api.route('/register', methods=['POST'])
class RegisterCoach(Resource):
    def post(self):
        try:
            if request.method == 'POST':
                data = request.get_json()
                print(data)
                print(data['id'])

                new_coach = CoachService.RegisterCoach(data)
                if new_coach:
                    return {'status': 200}
                return {'status': 400}
        except Exception as e:
            print(e)
            raise e


@coach_api.route('/search/<lon>:<lat>:<rad>', methods=['GET'])
class RetrieveAllCoachWithinRadius(Resource):
    def get(self, lon=None, lat=None, rad=None, sport=None):
        try:
            if request.method == 'GET':
                print(lon, lat, rad, sport)
                coaches = CoachService.CoachInRadius(int(rad), lon, lat)
                print(f"coaches  : {coaches}")
                list_id_coach = [coach.id_user for coach in coaches]
                print(list_id_coach)
                annonces = CoachService.GetAllAnnonceOfListOfCoach(list_id_coach)
                print(annonces)

                annonces_json = [
                    {key: value for key, value in annonce.__dict__.items() if
                     key != '_sa_instance_state'}
                    for annonce in annonces
                ]

                for annonce in annonces_json:
                    annonce['sport'] = ast.literal_eval(annonce['sport'])
                    
                print(annonces_json)
                return {'status': 200, 'annonce': annonces_json}
        except Exception as e:
            print(e)
            raise e
