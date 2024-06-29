from flask import request
from ..model import Contact
from flask_restx import Namespace, Resource
from ..service.contact_service import contact_service

contact_api = Namespace('contact api',
                        description='register contact information')


@contact_api.route('/send', methods=['POST'])
class SendContact(Resource):
    def post(self):
        if request.method == 'POST':
            try:
                data = request.get_json()
                contact = Contact(name=data['name'], email=data['email'],
                                  phone_number=data['phone_number'],
                                  message=data['message'])
                contact_service.saveContact(contact)
                return {"status": 200}
            except Exception as e:
                print(e)
                return {"status": 404}

