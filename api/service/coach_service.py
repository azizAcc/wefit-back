from api.model import Coach, User, Annonce
from api.model import SportIcon
from api.extensions import bcrypt, db
from sqlalchemy import func


class CoachService:
    def __init__(self):
        pass

    @staticmethod
    def RegisterCoach(data):
        try:
            best_sport_icon = SportIcon.query.filter_by(name=data['sport']).first().icon
            print(best_sport_icon)
            user = User.query.filter_by(id=data['id']).first()
            user.top_coach = 1
            new_coach = Coach(data['id'], data['adresse'], data['latitude'], data['longitude'],
                              data['sport'],
                              best_sport_icon,
                              data['genre'],
                              data['phone_number'])

            db.session.add(new_coach)
            db.session.commit()
            return new_coach
        except Exception as e:
            print(e)
            db.session.rollback()
            return False


    @staticmethod
    def getSingleCoach(id):
        try:
            coach = Coach.query.filter_by(id_user=id).first()
            if coach:
                return coach
            return None
        except Exception as e:
            raise e

    @staticmethod
    def CreateAnnonce(data):
        try:
            annonce = Annonce(data['id'],data['title'],data['description'],str(data['sports']),data['tarif'])
            db.session.add(annonce)
            db.session.commit()
            return annonce
        except Exception as e:
            print(e)
            db.session.rollback()
            return False

    @staticmethod
    def GetAllAnnoncesOfSingleCoach(id_coach):
        try:
            annonces = Annonce.query.filter_by(id_coach=id_coach).all()
            return annonces
        except Exception as e:
            print(e)


    @staticmethod
    def GetAllAnnonceOfListOfCoach(list_id):
        try:
            annonces = Annonce.query.filter(Annonce.id_coach.in_(list_id)).all()
            return annonces
        except Exception as e:
            print(e)
            raise e

    @staticmethod
    def DeleteAnnonce(id_annonce):
        try:
            annonce = Annonce.query.get(id_annonce)
            print(annonce)
            if annonce:
                db.session.delete(annonce)
                db.session.commit()
                return {'status': 200, 'message': 'deleted successfully'}
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def UpdateAnnonce(id_annonce, data):
        try:
            annonce = Annonce.query.get(id_annonce)
            if annonce:
                annonce.titre = data['titre']
                annonce.description = data['description']
                annonce.tarif = data['tarif']
                annonce.sport = str(data['sport'])
                db.session.commit()

                return annonce

        except Exception as e:
            db.session.rollback()
            raise e


    @staticmethod
    def CoachInRadius(radius, longitude, latitude):
        try:
            radius_m = radius/100
            results = db.session.query(Coach).filter(
                func.ST_DWithin(
                    func.ST_SetSRID(func.ST_MakePoint(longitude, latitude), 4326),  # Point to compare
                    Coach.geomcol,  # Column in the database
                    radius_m  # Distance in meters
                )
            ).all()

            print(str(db.session.query(Coach).filter(
                func.ST_DWithin(
                    func.ST_SetSRID(func.ST_MakePoint(longitude, latitude), 4326),
                    Coach.geomcol,
                    radius_m
                )
            ).statement))

            return results
        except Exception as e:
            print(e)
