from .theme import BLEU_NUIT, GRIS_TEXTE, GRIS_LIGNE
from .utils import texte, ligne


def dessiner_titre_section(c, numero, titre, x, y, largeur=460):
    texte(c, f"{numero}. {titre}", x, y, taille=9, couleur=BLEU_NUIT, gras=True)
    ligne(c, x, y - 7, x + largeur, y - 7, couleur=GRIS_LIGNE, epaisseur=0.6)

    # Important : espace suffisant entre le titre et le tableau
    return y - 26


def dessiner_petit_texte(c, contenu, x, y, largeur, taille=7):
    mots = str(contenu).split()
    ligne_actuelle = ""
    position_y = y

    for mot in mots:
        test = ligne_actuelle + " " + mot

        if len(test) > 75:
            texte(c, ligne_actuelle, x, position_y, taille=taille, couleur=GRIS_TEXTE)
            ligne_actuelle = mot
            position_y -= 10
        else:
            ligne_actuelle = test

    if ligne_actuelle:
        texte(c, ligne_actuelle, x, position_y, taille=taille, couleur=GRIS_TEXTE)

    return position_y - 12