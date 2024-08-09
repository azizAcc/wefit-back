from api.extensions import db, bcrypt
import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))

    def __init__(self, email, password):
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')


class Tracker(db.Model):
    id_track = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer)
    action = db.Column(db.String(255))
    description = db.Column(db.String(511))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)



class Payments(db.Model):
    id_payment = db.Column(db.Integer, primary_key=True, autoincrement=True)
    total = db.Column(db.Numeric(10, 2))
    id_link = db.Column(db.Integer)
    id_user = db.Column(db.Integer)


class Contact(db.Model):
    id_contact = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(155))
    email = db.Column(db.String(155))
    phone_number = db.Column(db.String(155))
    message = db.Column(db.String(511))
