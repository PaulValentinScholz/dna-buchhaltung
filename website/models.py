from . import db
from flask_login import UserMixin

class Bilanz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(512), nullable=False)
    anfangsbestand = db.Column(db.Float)
    abschlussbestand = db.Column(db.Float)
    kontoart = db.Column(db.String(128))
    kontotyp = db.Column(db.String(128), nullable=False)
    abgeschlossen = db.Column(db.Boolean, default=False)
    default_konto = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Buchungssatz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wert = db.Column(db.Integer, nullable=False)
    anmerkung = db.Column(db.String(256))
    soll_id = db.Column(db.Integer, db.ForeignKey('bilanz.id'), nullable=False)
    haben_id = db.Column(db.Integer, db.ForeignKey('bilanz.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128))
    name = db.Column(db.String(128))
    bilanzen = db.relationship('Bilanz')
    buchungssaetze = db.relationship('Buchungssatz')