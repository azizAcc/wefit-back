from flask_restx import Namespace, Resource
from flask import request, jsonify

from ..extensions import db
from api.model import WaitList

waitlist_api = Namespace(
    'waitlist',
    description='Waitlist controller'
)

@waitlist_api.route('/register', methods=['POST'])
class RegisterEmail(Resource):
    def post(self):
        try:
            if request.method == 'POST':
                data = request.get_json()
                if WaitList.query.filter_by(email=data['email']).first():
                    print("email existant")
                    return {'status': 400, 'message':'Vous êtes déjà enregistrer'}
                print(data)
                new_email = WaitList(data['email'],data['recherche'],data['coach'])
                db.session.add(new_email)
                db.session.commit()
                return {'status': 200}
        except Exception as e:
            db.session.rollback()
            raise e