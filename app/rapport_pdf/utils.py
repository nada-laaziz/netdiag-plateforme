from reportlab.pdfbase.pdfmetrics import stringWidth

from .theme import FONT_NORMAL, FONT_BOLD, GRIS_TEXTE


def texte(c, valeur, x, y, taille=8, couleur=None, gras=False):
    c.setFont(FONT_BOLD if gras else FONT_NORMAL, taille)

    if couleur:
        c.setFillColor(couleur)

    c.drawString(x, y, str(valeur))


def texte_centre(c, valeur, x, y, largeur, taille=8, couleur=None, gras=False):
    c.setFont(FONT_BOLD if gras else FONT_NORMAL, taille)

    if couleur:
        c.setFillColor(couleur)

    valeur = str(valeur)
    largeur_texte = stringWidth(valeur, FONT_BOLD if gras else FONT_NORMAL, taille)
    c.drawString(x + (largeur - largeur_texte) / 2, y, valeur)


def texte_droite(c, valeur, x, y, largeur, taille=8, couleur=None, gras=False):
    c.setFont(FONT_BOLD if gras else FONT_NORMAL, taille)

    if couleur:
        c.setFillColor(couleur)

    valeur = str(valeur)
    largeur_texte = stringWidth(valeur, FONT_BOLD if gras else FONT_NORMAL, taille)
    c.drawString(x + largeur - largeur_texte, y, valeur)


def ligne(c, x1, y1, x2, y2, couleur=GRIS_TEXTE, epaisseur=0.5):
    c.setStrokeColor(couleur)
    c.setLineWidth(epaisseur)
    c.line(x1, y1, x2, y2)