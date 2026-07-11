import pytest
from app import create_app, db


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SECRET_KEY": "cle-de-test"
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()
from app.models import Utilisateur
from app import db


def connecter_utilisateur_test(client, app, email="yasser@test.com", mot_de_passe="test1234"):
    with app.app_context():
        utilisateur = Utilisateur(nom="Yasser Test", email=email)
        utilisateur.definir_mot_de_passe(mot_de_passe)
        db.session.add(utilisateur)
        db.session.commit()
        id_utilisateur = utilisateur.id

    with client.session_transaction() as session:
        session['utilisateur_id'] = id_utilisateur

    return id_utilisateur