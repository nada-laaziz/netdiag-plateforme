from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class Utilisateur(db.Model):
    __tablename__ = 'utilisateurs'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mot_de_passe_hash = db.Column(db.String(255), nullable=False)

    def definir_mot_de_passe(self, mot_de_passe):
        self.mot_de_passe_hash = generate_password_hash(mot_de_passe)

    def verifier_mot_de_passe(self, mot_de_passe):
        return check_password_hash(self.mot_de_passe_hash, mot_de_passe)
class Projet(db.Model):
    __tablename__ = 'projets'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    id_utilisateur = db.Column(db.Integer, db.ForeignKey('utilisateurs.id'), nullable=False)

    utilisateur = db.relationship('Utilisateur', backref='projets')
class Equipement(db.Model):
    __tablename__ = 'equipements'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(150), nullable=False)
    type = db.Column(db.String(100), nullable=True)
    adresse_ip = db.Column(db.String(50), nullable=True)
    adresse_mac = db.Column(db.String(50), nullable=True)
    constructeur = db.Column(db.String(100), nullable=True)
    emplacement = db.Column(db.String(150), nullable=True)
    description = db.Column(db.String(500), nullable=True)
    id_projet = db.Column(db.Integer, db.ForeignKey('projets.id'), nullable=False)

    projet = db.relationship('Projet', backref='equipements')