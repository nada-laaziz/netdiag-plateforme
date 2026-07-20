# netdiag-plateforme
# NetDiag — Plateforme de gestion d'infrastructures réseau avec assistance au diagnostic

## Description

NetDiag est une plateforme web pédagogique destinée aux techniciens réseau, permettant de centraliser :
- la gestion de projets réseau et de leurs équipements
- la visualisation simplifiée de la topologie réseau
- l'analyse de captures Wireshark (.pcap / .pcapng)
- un diagnostic automatique basé sur des règles simples
- la génération d'un rapport PDF récapitulatif

Ce projet a été réalisé dans le cadre d'un stage de première année, par une étudiante en Génie Informatique et une étudiante en Cybersécurité.

## Fonctionnalités

- Authentification (connexion, inscription, déconnexion)
- Gestion des projets réseau (CRUD complet)
- Gestion des équipements (CRUD complet)
- Visualisation de la topologie réseau (SVG)
- Analyse de captures réseau (Scapy) : protocoles, IP, DNS, ICMP, conversations
- Détection d'anomalies : trafic non chiffré, scan de ports, SYN Flood, etc.
- Génération de rapport PDF (ReportLab)
- Suite de tests automatisés (Pytest)

## Stack technique

- **Backend** : Python, Flask
- **Base de données** : SQLite, SQLAlchemy (ORM)
- **Frontend** : HTML, CSS, Jinja2
- **Analyse réseau** : Scapy
- **Génération PDF** : ReportLab
- **Tests** : Pytest
- **Gestion de version** : Git / GitHub

## Installation

### Prérequis
- Python 3.10 ou supérieur
- Git

### Étapes

1. Cloner le dépôt
```bash
git clone https://github.com/nada-laaziz/netdiag-plateforme.git
cd netdiag-plateforme
```

2. Créer et activer un environnement virtuel
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

3. Installer les dépendances
```bash
pip install -r requirements.txt
```

4. Lancer l'application
```bash
python run.py
```

5. Ouvrir dans le navigateur 
http://localhost:5000

## Structure du projet
netdiag-plateforme/
├── app/
│   ├── models.py            # Modèles de base de données
│   ├── analyse_reseau/      # Lecture et analyse des fichiers PCAP
│   ├── analyseurs/          # Analyses spécialisées (DNS, ICMP, SYN Flood...)
│   ├── rapport_pdf/         # Génération du rapport PDF
│   ├── templates/           # Pages HTML
│   └── static/css/          # Styles
├── tests/                   # Tests automatisés (Pytest)
├── requirements.txt
└── run.py

## Tests

```bash
pytest -v
```

## Équipe

- Nada Laaziz — Génie Informatique — Interface, base de données, backend
- Douae Loukili — Cybersécurité — Analyse réseau, règles de diagnostic, génération PDF

## Limites connues

- L'application est un outil pédagogique, non destiné à remplacer des outils professionnels de supervision réseau
- Le diagnostic proposé est une aide à la décision basée sur des règles simples, non un diagnostic garanti
- La gestion des fichiers PCAP invalides n'affiche pas encore toujours un message d'erreur convivial (amélioration prévue)