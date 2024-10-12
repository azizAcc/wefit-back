from api.extensions import db, bcrypt
import datetime


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    top_coach = db.Column(db.Integer)

    def __init__(self, email, password):
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

class Coach(db.Model):
    __tablename__ = 'coach'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(255))
    surname = db.Column(db.String(255))
    titre = db.Column(db.String)
    description = db.Column(db.String)
    genre = db.Column(db.String(255))
    image_url = db.Column(db.String(255))
    best_sport = db.Column(db.String(255))
    best_sport_icon = db.Column(db.String(255))
    sport = db.Column(db.String)
    isHover = db.Column(db.Boolean)
    nb_avis = db.Column(db.Integer)
    rating = db.Column(db.Float)
    tarif = db.Column(db.Float)

class SportIcon(db.Model):
    __tablename__ = 'sport_icon'
    name = db.Column(db.String(255))
    icon = db.Column(db.String(255))