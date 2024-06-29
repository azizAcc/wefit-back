from ..model import Tracker
from ..extensions import db


class tracking_service:
    def __init__(self):
        pass

    @staticmethod
    def registerTracking(tracker: Tracker):
        try:
            db.session.add(tracker)
            db.session.commit()
            print("tracking commit success")
        except Exception as e:
            raise e
