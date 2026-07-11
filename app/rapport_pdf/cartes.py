from .theme import BLANC, BLEU, FONT_BOLD


def dessiner_carte(c, x, y, largeur, hauteur, titre, valeur, sous_titre="", couleur=BLEU):
    c.setFillColor(couleur)
    c.roundRect(x, y, largeur, hauteur, 6, fill=1, stroke=0)

    c.setFillColor(BLANC)
    c.setFont(FONT_BOLD, 8)
    c.drawCentredString(x + largeur / 2, y + hauteur - 16, str(titre))

    c.setFont(FONT_BOLD, 15)
    c.drawCentredString(x + largeur / 2, y + hauteur / 2 - 3, str(valeur))

    if sous_titre:
        c.setFont(FONT_BOLD, 6.5)
        c.drawCentredString(x + largeur / 2, y + 10, str(sous_titre))