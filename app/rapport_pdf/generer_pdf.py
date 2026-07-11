from datetime import datetime

from reportlab.pdfgen import canvas

from .theme import (
    PAGE_SIZE,
    PAGE_WIDTH,
    PAGE_HEIGHT,
    MARGIN_X,
    MARGIN_TOP,
    BLEU_NUIT,
    BLEU,
    GRIS_TEXTE,
    GRIS_FOND,
    BLANC,
    couleur_score,
    couleur_alerte,
    FONT_BOLD,
    FONT_NORMAL,
)
from .utils import texte, texte_droite
from .cartes import dessiner_carte
from .tableaux import dessiner_tableau
from .graphiques import (
    dessiner_barre_score,
    dessiner_barres_horizontales,
    dessiner_donut_protocoles,
)
from .sections import dessiner_titre_section, dessiner_petit_texte


def top_items(dictionnaire, limite=5):
    return sorted(
        dictionnaire.items(),
        key=lambda x: x[1],
        reverse=True
    )[:limite]


def nouvelle_page(c):
    c.showPage()
    c.setFillColor(GRIS_FOND)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
    return PAGE_HEIGHT - MARGIN_TOP


def generer_recommandations(alertes):
    recommandations = []

    for alerte in alertes:
        titre = alerte.get("titre", "").lower()

        if "http" in titre:
            recommandations.append(
                "Privilégier HTTPS et limiter les flux non chiffrés."
            )

        elif "beaucoup de machines" in titre:
            recommandations.append(
                "Vérifier la machine qui communique avec beaucoup d'hôtes."
            )

        elif "dominante" in titre:
            recommandations.append(
                "Surveiller la conversation réseau dominante."
            )

        elif "scan de ports" in titre:
            recommandations.append(
                "Contrôler les ports ouverts sur la machine suspecte."
            )

        elif "syn flood" in titre:
            recommandations.append(
                "Vérifier les connexions TCP et les protections anti-DDoS."
            )

    recommandations_uniques = list(dict.fromkeys(recommandations))

    if not recommandations_uniques:
        recommandations_uniques.append(
            "Aucune action urgente. Continuer la surveillance du réseau."
        )

    return recommandations_uniques[:5]


def generer_pdf(resultats, chemin_pdf):
    c = canvas.Canvas(chemin_pdf, pagesize=PAGE_SIZE)

    diagnostic = resultats.get("diagnostic_final", {})
    score = diagnostic.get("score", 0)
    statut = diagnostic.get("statut", "Non disponible")
    message = diagnostic.get("message", "Non disponible")
    alertes = resultats.get("alertes", [])
    stats = resultats.get("statistiques", {})
    protocoles = resultats.get("protocoles", {})
    total_paquets = resultats.get("nombre_paquets", 0)

    couleur_principale = couleur_score(score)

    x = MARGIN_X
    y = PAGE_HEIGHT - MARGIN_TOP
    largeur_contenu = 460

    c.setFillColor(GRIS_FOND)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)

    c.setFillColor(BLEU_NUIT)
    c.roundRect(x, y - 55, largeur_contenu, 55, 10, fill=1, stroke=0)

    c.setFillColor(BLANC)
    c.setFont(FONT_BOLD, 20)
    c.drawString(x + 18, y - 25, "NETDIAG")

    c.setFont(FONT_NORMAL, 8)
    c.drawString(x + 18, y - 40, "Rapport de diagnostic réseau")

    texte_droite(
        c,
        datetime.now().strftime("%d/%m/%Y à %H:%M"),
        x,
        y - 32,
        largeur_contenu - 18,
        taille=8,
        couleur=BLANC
    )

    y -= 78

    largeur_carte = (largeur_contenu - 24) / 4
    hauteur_carte = 58

    dessiner_carte(c, x, y - hauteur_carte, largeur_carte, hauteur_carte, "Score réseau", f"{score}/100", statut, couleur_principale)
    dessiner_carte(c, x + largeur_carte + 8, y - hauteur_carte, largeur_carte, hauteur_carte, "Paquets", total_paquets, "analysés", BLEU)
    dessiner_carte(c, x + 2 * (largeur_carte + 8), y - hauteur_carte, largeur_carte, hauteur_carte, "IP sources", len(resultats.get("ip_sources", {})), "détectées", BLEU)
    dessiner_carte(c, x + 3 * (largeur_carte + 8), y - hauteur_carte, largeur_carte, hauteur_carte, "Alertes", len(alertes), "détectées", BLEU)

    y -= 82

    dessiner_barre_score(c, x, y - 12, largeur_contenu, 10, score, couleur_principale)

    y -= 42

    c.setFillColor(BLANC)
    c.roundRect(x, y - 64, largeur_contenu, 64, 8, fill=1, stroke=0)

    texte(c, "Résumé automatique", x + 12, y - 18, taille=9, couleur=BLEU_NUIT, gras=True)
    dessiner_petit_texte(c, message, x + 12, y - 34, largeur_contenu - 24, taille=7)

    y -= 86

    y = dessiner_titre_section(c, "1", "Vue graphique", x, y, largeur_contenu)

    gauche_x = x
    droite_x = x + 240

    c.setFillColor(BLANC)
    c.roundRect(gauche_x, y - 142, 220, 142, 8, fill=1, stroke=0)

    texte(c, "Répartition des protocoles", gauche_x + 12, y - 18, taille=8, couleur=BLEU_NUIT, gras=True)
    dessiner_donut_protocoles(c, gauche_x + 60, y - 125, 86, protocoles)

    c.setFillColor(BLANC)
    c.roundRect(droite_x, y - 142, 220, 142, 8, fill=1, stroke=0)

    texte(c, "Top IP sources", droite_x + 12, y - 18, taille=8, couleur=BLEU_NUIT, gras=True)
    dessiner_barres_horizontales(
        c,
        droite_x + 12,
        y - 42,
        top_items(resultats.get("ip_sources", {}), 5),
        largeur=85,
        hauteur_barre=7,
        espace=19
    )

    y -= 166

    y = dessiner_titre_section(c, "2", "Statistiques générales", x, y, largeur_contenu)

    lignes_stats = [
        ["Nombre de paquets", total_paquets],
        ["Nombre d'IP sources", len(resultats.get("ip_sources", {}))],
        ["Nombre d'IP destinations", len(resultats.get("ip_destinations", {}))],
        ["Protocole dominant", stats.get("protocole_dominant", "Non disponible")],
    ]

    y = dessiner_tableau(
        c, x, y,
        [230, 230],
        20,
        ["Indicateur", "Valeur"],
        lignes_stats
    ) - 18

    y = dessiner_titre_section(c, "3", "Protocoles détectés", x, y, largeur_contenu)

    lignes_protocoles = []

    for protocole, nombre in protocoles.items():
        if nombre > 0:
            pourcentage = (nombre / total_paquets) * 100 if total_paquets else 0
            lignes_protocoles.append([protocole, nombre, f"{pourcentage:.1f}%"])

    y = dessiner_tableau(
        c, x, y,
        [150, 150, 160],
        19,
        ["Protocole", "Paquets", "Pourcentage"],
        lignes_protocoles
    ) - 18

    if y < 170:
        y = nouvelle_page(c)

    y = dessiner_titre_section(c, "4", "Top domaines DNS", x, y, largeur_contenu)

    lignes_dns = []
    dns = resultats.get("dns", {})

    for domaine, nombre in dns.get("top_domaines", []):
        lignes_dns.append([domaine, nombre])

    if not lignes_dns:
        lignes_dns.append(["Aucun domaine détecté", 0])

    y = dessiner_tableau(
        c, x, y,
        [320, 140],
        19,
        ["Domaine", "Requêtes"],
        lignes_dns
    ) - 18

    y = dessiner_titre_section(c, "5", "Top conversations", x, y, largeur_contenu)

    lignes_conv = []

    for conv in resultats.get("top_conversations", []):
        paquets = conv.get("paquets", 0)
        pourcentage = (paquets / total_paquets) * 100 if total_paquets else 0
        lignes_conv.append([
            conv.get("ip_1", ""),
            conv.get("ip_2", ""),
            paquets,
            f"{pourcentage:.1f}%"
        ])

    y = dessiner_tableau(
        c, x, y,
        [125, 125, 105, 105],
        19,
        ["IP 1", "IP 2", "Paquets", "%"],
        lignes_conv
    ) - 18

    if y < 220:
        y = nouvelle_page(c)

    y = dessiner_titre_section(c, "6", "Analyses sécurité", x, y, largeur_contenu)

    syn = resultats.get("syn_flood", {})
    icmp = resultats.get("icmp", {})
    scan_ports = resultats.get("scan_ports", [])

    lignes_sec = [
        ["SYN Flood", "Suspect" if syn.get("suspect") else "Aucun SYN Flood détecté"],
        ["Paquets SYN", syn.get("syn", 0)],
        ["Paquets ACK", syn.get("ack", 0)],
        ["ICMP", f"{icmp.get('total_icmp', 0)} paquet(s)"],
        ["Scan de ports", "Suspect détecté" if scan_ports else "Aucun scan suspect"],
    ]

    y = dessiner_tableau(
        c, x, y,
        [180, 280],
        19,
        ["Analyse", "Résultat"],
        lignes_sec
    ) - 18

    y = dessiner_titre_section(c, "7", "Alertes détectées", x, y, largeur_contenu)

    if alertes:
        for alerte in alertes[:6]:
            niveau = alerte.get("niveau", "")
            couleur = couleur_alerte(niveau)

            c.setFillColor(BLANC)
            c.roundRect(x, y - 44, largeur_contenu, 44, 7, fill=1, stroke=0)

            c.setFillColor(couleur)
            c.roundRect(x + 10, y - 29, 52, 17, 6, fill=1, stroke=0)

            c.setFillColor(BLANC)
            c.setFont(FONT_BOLD, 6.5)
            c.drawCentredString(x + 36, y - 23, niveau)

            texte(c, alerte.get("titre", ""), x + 75, y - 18, taille=7.5, couleur=BLEU_NUIT, gras=True)
            dessiner_petit_texte(c, alerte.get("description", ""), x + 75, y - 31, 360, taille=6.5)

            y -= 52
    else:
        texte(c, "Aucune alerte détectée.", x, y, taille=8, couleur=GRIS_TEXTE)
        y -= 20

    if y < 160:
        y = nouvelle_page(c)

    y = dessiner_titre_section(c, "8", "Diagnostic final", x, y, largeur_contenu)

    c.setFillColor(BLANC)
    c.roundRect(x, y - 68, largeur_contenu, 68, 8, fill=1, stroke=0)

    texte(c, f"Score : {score}/100", x + 12, y - 18, taille=8, couleur=BLEU_NUIT, gras=True)
    texte(c, f"Statut : {statut}", x + 12, y - 32, taille=8, couleur=BLEU_NUIT, gras=True)
    dessiner_petit_texte(c, message, x + 12, y - 47, largeur_contenu - 24, taille=6.8)

    y -= 88

    y = dessiner_titre_section(c, "9", "Recommandations", x, y, largeur_contenu)

    recommandations = generer_recommandations(alertes)

    for rec in recommandations:
        texte(c, f"✓ {rec}", x + 8, y, taille=7, couleur=GRIS_TEXTE)
        y -= 13

    c.setFillColor(GRIS_TEXTE)
    c.setFont(FONT_NORMAL, 6.5)
    c.drawCentredString(PAGE_WIDTH / 2, 18, "NETDIAG - Rapport automatique généré à partir d'une capture Wireshark")

    c.save()