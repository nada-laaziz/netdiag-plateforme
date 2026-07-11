from tests.conftest import connecter_utilisateur_test
from app.models import Projet
from app import db


def test_topologie_sans_equipement(app, client):
    id_utilisateur = connecter_utilisateur_test(client, app)

    with app.app_context():
        projet = Projet(nom="Reseau Vide", description="", id_utilisateur=id_utilisateur)
        db.session.add(projet)
        db.session.commit()
        id_projet = projet.id

    reponse = client.get(f'/projets/{id_projet}/topologie')

    assert reponse.status_code == 200
    assert 'Aucun équipement'.encode('utf-8') in reponse.data