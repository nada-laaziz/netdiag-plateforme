from tests.conftest import connecter_utilisateur_test
from app.models import Projet
from app import db


def creer_projet_test(app, id_utilisateur, nom="Projet Test"):
    with app.app_context():
        projet = Projet(nom=nom, description="", id_utilisateur=id_utilisateur)
        db.session.add(projet)
        db.session.commit()
        return projet.id


def test_ajouter_un_equipement(app, client):
    id_utilisateur = connecter_utilisateur_test(client, app)
    id_projet = creer_projet_test(app, id_utilisateur)

    reponse = client.post(f'/projets/{id_projet}/equipements/nouveau', data={
        'nom': 'Routeur Test',
        'type': 'routeur',
        'adresse_ip': '192.168.1.1',
        'adresse_mac': '',
        'constructeur': '',
        'emplacement': '',
        'description': ''
    }, follow_redirects=True)

    assert reponse.status_code == 200
    assert b'Routeur Test' in reponse.data


def test_page_equipements_liste_bien_le_projet(app, client):
    id_utilisateur = connecter_utilisateur_test(client, app)
    id_projet = creer_projet_test(app, id_utilisateur, nom="Reseau Bureau")

    reponse = client.get(f'/projets/{id_projet}/equipements')

    assert reponse.status_code == 200
    assert b'Reseau Bureau' in reponse.data