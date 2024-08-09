from api.model import User
from api.extensions import bcrypt, db


class AuthService:

    @staticmethod
    def user_exist(email):
        try:
            if User.query.filter_by(email=email).first():
                return True
            return False
        except Exception as e:
            print(e)

    @staticmethod
    def loginService(_email,_password):
        try:
            user = User.query.filter_by(email=_email).first()
            if user and bcrypt.check_password_hash(user.password, _password):
                return user
        except Exception as e:
            print(e)

    @staticmethod
    def registerService(data):
        try:
            user = User(email=data['email'], password=data['password'])
            db.session.add(user)
            db.session.commit()
            return user
        except Exception as e:
            print(e)

    @staticmethod
    def getAllUsers():
        return User.query.all()
