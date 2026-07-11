from .theme import BLEU, BLEU_2, BLEU_CLAIR, GRIS_CLAIR, GRIS_TEXTE, FONT_BOLD, FONT_NORMAL


def dessiner_barre_score(c, x, y, largeur, hauteur, score, couleur):
    c.setFillColor(GRIS_CLAIR)
    c.roundRect(x, y, largeur, hauteur, 5, fill=1, stroke=0)

    largeur_score = largeur * (score / 100)

    c.setFillColor(couleur)
    c.roundRect(x, y, largeur_score, hauteur, 5, fill=1, stroke=0)

    c.setFillColor(GRIS_TEXTE)
    c.setFont(FONT_BOLD, 7)
    c.drawString(x, y + hauteur + 5, "Score global du réseau")


def dessiner_barres_horizontales(c, x, y, donnees, largeur=160, hauteur_barre=8, espace=14):
    if not donnees:
        return y

    valeur_max = max([valeur for _, valeur in donnees])

    position_y = y

    for label, valeur in donnees:
        c.setFillColor(GRIS_TEXTE)
        c.setFont(FONT_NORMAL, 6)
        c.drawString(x, position_y + 2, str(label)[:24])

        c.setFillColor(BLEU_CLAIR)
        c.roundRect(x + 80, position_y, largeur, hauteur_barre, 3, fill=1, stroke=0)

        largeur_valeur = (valeur / valeur_max) * largeur if valeur_max > 0 else 0

        c.setFillColor(BLEU)
        c.roundRect(x + 80, position_y, largeur_valeur, hauteur_barre, 3, fill=1, stroke=0)

        c.setFillColor(GRIS_TEXTE)
        c.setFont(FONT_BOLD, 6)
        c.drawString(x + 85 + largeur, position_y + 1, str(valeur))

        position_y -= espace

    return position_y


def dessiner_donut_protocoles(c, x, y, taille, protocoles):
    total = sum([v for v in protocoles.values() if v > 0])

    if total == 0:
        return

    couleurs = [BLEU, BLEU_2, GRIS_CLAIR, BLEU_CLAIR]
    debut = 90
    i = 0

    for protocole, valeur in protocoles.items():
        if valeur <= 0:
            continue

        angle = (valeur / total) * 360
        c.setFillColor(couleurs[i % len(couleurs)])
        c.wedge(x, y, x + taille, y + taille, debut, debut + angle, fill=1, stroke=0)
        debut += angle
        i += 1

    c.setFillColor("white")
    marge = taille * 0.28
    c.circle(x + taille / 2, y + taille / 2, taille / 2 - marge, fill=1, stroke=0)

    c.setFillColor(GRIS_TEXTE)
    c.setFont(FONT_BOLD, 7)
    c.drawCentredString(x + taille / 2, y + taille / 2 + 3, "Protocoles")

    c.setFont(FONT_NORMAL, 6)
    c.drawCentredString(x + taille / 2, y + taille / 2 - 7, f"{int(total)} paquets")