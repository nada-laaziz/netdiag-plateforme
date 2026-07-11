from app.models import Utilisateur
from app import db


def creer_utilisateur_test(app, email="yasser@test.com", mot_de_passe="test1234"):
    with app.app_context():
        utilisateur = Utilisateur(nom="Yasser Test", email=email)
        utilisateur.definir_mot_de_passe(mot_de_passe)
        db.session.add(utilisateur)
        db.session.commit()


def test_page_login_accessible(client):
    reponse = client.get('/login')
    assert reponse.status_code == 200


def test_connexion_avec_bons_identifiants(app, client):
    creer_utilisateur_test(app)

    reponse = client.post('/login', data={
        'email': 'yasser@test.com',
        'password': 'test1234'
    }, follow_redirects=True)

    assert reponse.status_code == 200
    assert b'Mes projets' in reponse.data


def test_connexion_avec_mauvais_mot_de_passe(app, client):
    creer_utilisateur_test(app)

    reponse = client.post('/login', data={
        'email': 'yasser@test.com',
        'password': 'mauvais_mot_de_passe'
    })

    assert b'incorrect' in reponse.data


def test_acces_projets_sans_connexion_redirige(client):
    reponse = client.get('/projets', follow_redirects=False)

    assert reponse.status_code == 302
    assert '/login' in reponse.headers['Location']


def test_inscription_avec_email_deja_utilise(app, client):
    creer_utilisateur_test(app, email="deja@test.com")

    reponse = client.post('/register', data={
        'nom': 'Autre Personne',
        'email': 'deja@test.com',
        'password': 'motdepasse'
    })

    assert 'existe déjà'.encode('utf-8') in reponse.data