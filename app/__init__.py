from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///netdiag.db'
    app.config['SECRET_KEY'] = 'a-changer-plus-tard'

    db.init_app(app)

    from app.models import Utilisateur

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
        return "Page des projets (à construire au module 2)"

    return app
