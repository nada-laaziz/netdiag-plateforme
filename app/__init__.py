from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///netdiag.db'
    app.config['SECRET_KEY'] = 'a-changer-plus-tard'

    db.init_app(app)

    from app.models import Utilisateur, Projet

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
    return app
