from api.model import User
from api.extensions import bcrypt, db

class UserService:
    def __init__(self):
        pass

    @staticmethod
    def UpdateInformation(data):
        try:
            user = User.query.filter_by(email=data['old_email']).first()

            user.email = data['email']
            user.nom = data['nom']
            user.prenom = data['prenom']
            db.session.commit()
            print(user)
            return user

        except Exception as e:
            print(e)
            db.session.rollback()
            return False

