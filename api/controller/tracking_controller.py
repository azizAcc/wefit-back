from ..model import Tracker
from flask_restx import Resource, Namespace
from flask import request
from ..service.tracking_service import tracking_service

api_tracker = Namespace(
    'tracker',
    description='track user actions'
)


@api_tracker.route('/track', methods=['POST'])
class TrackingController(Resource):

    def post(self, action=None, desc=None):
        if request.method == 'POST':
            try:
                data = request.get_json()
                tracker = Tracker(id_user=data['id_user'], action=data['action'], description=data['description'])
                tracking_service.registerTracking(tracker)
                return {"status": 200}
            except Exception as e:
                print(e)
                return {"status": 404}
