from api.extensions import db, bcrypt
import datetime
from geoalchemy2 import Geometry


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    nom = db.Column(db.String(255))
    prenom = db.Column(db.String(255))
    image_url = db.Column(db.String(255))
    top_coach = db.Column(db.Integer)
    numero_tel = db.Column(db.String(255))

    def __init__(self, email, password):
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.top_coach = 0

class Coach(db.Model):
    __tablename__ = 'coach'

    id_user = db.Column(db.Integer,db.ForeignKey('users.id'), primary_key=True)
    adresse = db.Column(db.String(255))
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    geomcol = db.Column(
        Geometry(geometry_type="POINT", srid=4326),
        db.Computed("ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)", persisted=True)
    )
    tel_pro = db.Column(db.String(255))
    genre = db.Column(db.String(255))
    best_sport = db.Column(db.String(255))
    best_sport_icon = db.Column(db.String(255))
    #isHover = db.Column(db.Boolean)
    nb_avis = db.Column(db.Integer)
    rating = db.Column(db.Float)

    def __init__(self, id_user, adresse, latitude, longitude,sport, best_sport, genre, tel_pro):
        self.id_user = id_user
        self.adresse = adresse
        self.latitude = latitude
        self.longitude = longitude
        self.best_sport = sport
        self.best_sport_icon = best_sport
        self.nb_avis = 0
        self.rating = -1
        self.genre = genre
        self.tel_pro = tel_pro

class Annonce(db.Model):
    __tablename__ = 'annonce'
    id_annonce = db.Column(db.Integer, primary_key=True)
    id_coach = db.Column(db.Integer,db.ForeignKey('users.id'), nullable=False)
    titre = db.Column(db.String)
    description = db.Column(db.String)
    sport = db.Column(db.String)
    tarif = db.Column(db.Float)

    def __init__(self, id_coach, titre, description, sport, tarif):
        self.id_coach = id_coach
        self.titre = titre
        self.description = description
        self.sport = sport
        self.tarif = tarif


class SportIcon(db.Model):
    __tablename__ = 'sport_icon'
    name = db.Column(db.String(255), primary_key=True)
    icon = db.Column(db.String(255))

class Spatial(db.Model):
    __tablename__ = 'spatial_ref_sys'

    srid = db.Column(db.Integer, primary_key=True)
    srtext = db.Column(db.String(2048))
    auth_name = db.Column(db.String(256))
    proj4text = db.Column(db.String(2048))
    auth_srid = db.Column(db.Integer)

class WaitList(db.Model):
    __tablename__ = 'wait_list'
    email = db.Column(db.String(255), primary_key=True)
    recherche_coach = db.Column(db.Integer)
    est_coach = db.Column(db.Integer)

    def __init__(self, email, recherche_coach, est_coach):
        self.email = email
        self.recherche_coach = 1 if recherche_coach else 0
        self.est_coach = 1 if est_coach else 0