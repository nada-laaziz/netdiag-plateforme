import os
from werkzeug.utils import secure_filename
from app.analyse_reseau.pcap_reader import analyser_pcap
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import math

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///netdiag.db'
    app.config['SECRET_KEY'] = 'a-changer-plus-tard'

    db.init_app(app)
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    from app.models import Utilisateur, Projet, Equipement, Capture, Diagnostic

    with app.app_context():
        db.create_all()

    @app.route('/')
    @app.route('/login', methods=['GET'])
    def login():
        return render_template('login.html')

    @app.route('/login', methods=['POST'])
    def login_post():
        email = request.form.get('email')
        mot_de_passe = request.form.get('password')

        utilisateur = Utilisateur.query.filter_by(email=email).first()

        if utilisateur is None or not utilisateur.verifier_mot_de_passe(mot_de_passe):
            return render_template('login.html', erreur="Email ou mot de passe incorrect")

        session['utilisateur_id'] = utilisateur.id
        return redirect(url_for('projets'))

    @app.route('/logout')
    def logout():
        session.pop('utilisateur_id', None)
        return redirect(url_for('login'))
    @app.route('/register', methods=['GET'])
    def register():
        return render_template('register.html')

    @app.route('/register', methods=['POST'])
    def register_post():
        nom = request.form.get('nom')
        email = request.form.get('email')
        mot_de_passe = request.form.get('password')

        utilisateur_existant = Utilisateur.query.filter_by(email=email).first()
        if utilisateur_existant is not None:
            return render_template('register.html', erreur="Un compte existe déjà avec cet email")

        nouvel_utilisateur = Utilisateur(nom=nom, email=email)
        nouvel_utilisateur.definir_mot_de_passe(mot_de_passe)
        db.session.add(nouvel_utilisateur)
        db.session.commit()

        session['utilisateur_id'] = nouvel_utilisateur.id
        return redirect(url_for('projets'))
    @app.route('/projets')
    def projets():
        if 'utilisateur_id' not in session:
            return redirect(url_for('login'))

        utilisateur_id_connecte = session['utilisateur_id']
        liste_projets = Projet.query.filter_by(id_utilisateur=utilisateur_id_connecte).all()

        return render_template('projets.html', projets=liste_projets)
    @app.route('/projets/nouveau', methods=['GET', 'POST'])
    def nouveau_projet():
        if 'utilisateur_id' not in session:
            return redirect(url_for('login'))

        if request.method == 'POST':
            nom = request.form.get('nom')
            description = request.form.get('description')
            utilisateur_id_connecte = session['utilisateur_id']

            nouveau = Projet(
                nom=nom,
                description=description,
                id_utilisateur=utilisateur_id_connecte
            )
            db.session.add(nouveau)
            db.session.commit()

            return redirect(url_for('projets'))

        return render_template('nouveau_projet.html')
    @app.route('/projets/<int:id>/modifier', methods=['GET', 'POST'])
    def modifier_projet(id):
        if 'utilisateur_id' not in session:
            return redirect(url_for('login'))

        projet = Projet.query.get_or_404(id)

        if projet.id_utilisateur != session['utilisateur_id']:
            return redirect(url_for('projets'))

        if request.method == 'POST':
            projet.nom = request.form.get('nom')
            projet.description = request.form.get('description')
            db.session.commit()
            return redirect(url_for('projets'))

        return render_template('nouveau_projet.html', projet=projet)

    @app.route('/projets/<int:id>/supprimer', methods=['POST'])
    def supprimer_projet(id):
        if 'utilisateur_id' not in session:
            return redirect(url_for('login'))

        projet = Projet.query.get_or_404(id)

        if projet.id_utilisateur != session['utilisateur_id']:
            return redirect(url_for('projets'))

        db.session.delete(projet)
        db.session.commit()
        return redirect(url_for('projets'))
    @app.route('/projets/<int:id_projet>/equipements')
    def equipements_projet(id_projet):
        if 'utilisateur_id' not in session:
            return redirect(url_for('login'))

        projet = Projet.query.get_or_404(id_projet)

        if projet.id_utilisateur != session['utilisateur_id']:
            return redirect(url_for('projets'))

        liste_equipements = Equipement.query.filter_by(id_projet=id_projet).all()

        return render_template('equipements.html', projet=projet, equipements=liste_equipements)
    @app.route('/projets/<int:id_projet>/equipements/nouveau', methods=['GET', 'POST'])
    def nouvel_equipement(id_projet):
        if 'utilisateur_id' not in session:
            return redirect(url_for('login'))

        projet = Projet.query.get_or_404(id_projet)

        if projet.id_utilisateur != session['utilisateur_id']:
            return redirect(url_for('projets'))

        if request.method == 'POST':
            nouveau = Equipement(
                nom=request.form.get('nom'),
                type=request.form.get('type'),
                adresse_ip=request.form.get('adresse_ip'),
                adresse_mac=request.form.get('adresse_mac'),
                constructeur=request.form.get('constructeur'),
                emplacement=request.form.get('emplacement'),
                description=request.form.get('description'),
                id_projet=id_projet
            )
            db.session.add(nouveau)
            db.session.commit()
            return redirect(url_for('equipements_projet', id_projet=id_projet))

        return render_template('nouvel_equipement.html', id_projet=id_projet, equipement=None)

    @app.route('/equipements/<int:id>/modifier', methods=['GET', 'POST'])
    def modifier_equipement(id):
        if 'utilisateur_id' not in session:
            return redirect(url_for('login'))

        equipement = Equipement.query.get_or_404(id)

        if equipement.projet.id_utilisateur != session['utilisateur_id']:
            return redirect(url_for('projets'))

        if request.method == 'POST':
            equipement.nom = request.form.get('nom')
            equipement.type = request.form.get('type')
            equipement.adresse_ip = request.form.get('adresse_ip')
            equipement.adresse_mac = request.form.get('adresse_mac')
            equipement.constructeur = request.form.get('constructeur')
            equipement.emplacement = request.form.get('emplacement')
            equipement.description = request.form.get('description')
            db.session.commit()
            return redirect(url_for('equipements_projet', id_projet=equipement.id_projet))

        return render_template('nouvel_equipement.html', id_projet=equipement.id_projet, equipement=equipement)

    @app.route('/equipements/<int:id>/supprimer', methods=['POST'])
    def supprimer_equipement(id):
        if 'utilisateur_id' not in session:
            return redirect(url_for('login'))

        equipement = Equipement.query.get_or_404(id)

        if equipement.projet.id_utilisateur != session['utilisateur_id']:
            return redirect(url_for('projets'))

        id_projet = equipement.id_projet
        db.session.delete(equipement)
        db.session.commit()
        return redirect(url_for('equipements_projet', id_projet=id_projet))
    @app.route('/projets/<int:id_projet>/topologie')
    def topologie_projet(id_projet):
        if 'utilisateur_id' not in session:
            return redirect(url_for('login'))

        projet = Projet.query.get_or_404(id_projet)

        if projet.id_utilisateur != session['utilisateur_id']:
            return redirect(url_for('projets'))

        liste_equipements = Equipement.query.filter_by(id_projet=id_projet).all()

        equipements_positions = []
        nombre = len(liste_equipements)

        for index, eq in enumerate(liste_equipements):
            angle = (index * 360 / nombre) * (math.pi / 180)
            x = 300 + 180 * math.cos(angle)
            y = 250 + 180 * math.sin(angle)

            equipements_positions.append({
                'nom': eq.nom,
                'ip': eq.adresse_ip or '',
                'x': round(x),
                'y': round(y)
            })

        return render_template('topologie.html', projet=projet, equipements_positions=equipements_positions)
    @app.route('/projets/<int:id_projet>/analyse', methods=['GET', 'POST'])
    def analyse_projet(id_projet):
        if 'utilisateur_id' not in session:
            return redirect(url_for('login'))

        projet = Projet.query.get_or_404(id_projet)

        if projet.id_utilisateur != session['utilisateur_id']:
            return redirect(url_for('projets'))

        resultats = None

        if request.method == 'POST':
            fichier = request.files.get('fichier_pcap')

            if fichier and fichier.filename != '':
                nom_fichier = secure_filename(fichier.filename)
                chemin = os.path.join(app.config['UPLOAD_FOLDER'], nom_fichier)
                fichier.save(chemin)

                resultats = analyser_pcap(chemin)

                nouvelle_capture = Capture(
                    nom_fichier=nom_fichier,
                    nb_paquets=resultats['nombre_paquets'],
                    id_projet=id_projet
                )
                db.session.add(nouvelle_capture)
                db.session.commit()

                for alerte in resultats['alertes']:
                    diagnostic = Diagnostic(
                        niveau=alerte['niveau'],
                        titre=alerte['titre'],
                        description=alerte['description'],
                        id_capture=nouvelle_capture.id
                    )
                    db.session.add(diagnostic)
                db.session.commit()

        return render_template('analyse.html', projet=projet, resultats=resultats)
    return app
