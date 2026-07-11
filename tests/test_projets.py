from tests.conftest import connecter_utilisateur_test
from app.models import Projet
from app import db


def test_liste_projets_vide_au_depart(app, client):
    connecter_utilisateur_test(client, app)

    reponse = client.get('/projets')

    assert reponse.status_code == 200
    assert 'aucun projet'.encode('utf-8') in reponse.data


def test_creer_un_projet(app, client):
    connecter_utilisateur_test(client, app)

    reponse = client.post('/projets/nouveau', data={
        'nom': 'Reseau Test',
        'description': 'Un projet de test'
    }, follow_redirects=True)

    assert reponse.status_code == 200
    assert b'Reseau Test' in reponse.data


def test_projet_appartient_au_bon_utilisateur(app, client):
    id_utilisateur_1 = connecter_utilisateur_test(client, app, email="user1@test.com")

    with app.app_context():
        projet = Projet(nom="Projet privé", description="", id_utilisateur=id_utilisateur_1)
        db.session.add(projet)
        db.session.commit()
        id_projet = projet.id

    with client.session_transaction() as session:
        session.clear()

    connecter_utilisateur_test(client, app, email="user2@test.com")

    reponse = client.get(f'/projets/{id_projet}/modifier')

    assert reponse.status_code in (302, 404)


def test_supprimer_un_projet(app, client):
    connecter_utilisateur_test(client, app)

    client.post('/projets/nouveau', data={'nom': 'A supprimer', 'description': ''})

    with app.app_context():
        projet = Projet.query.filter_by(nom='A supprimer').first()
        id_projet = projet.id

    client.post(f'/projets/{id_projet}/supprimer', follow_redirects=True)

    with app.app_context():
        projet_encore_present = Projet.query.get(id_projet)
        assert projet_encore_present is None