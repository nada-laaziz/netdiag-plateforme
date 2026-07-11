from .theme import BLEU_NUIT, BLANC, GRIS_FOND, GRIS_LIGNE, FONT_NORMAL, FONT_BOLD


def dessiner_tableau(c, x, y, largeur_colonnes, hauteur_ligne, entetes, lignes):
    largeur_totale = sum(largeur_colonnes)

    c.setFillColor(BLEU_NUIT)
    c.rect(x, y, largeur_totale, hauteur_ligne, fill=1, stroke=0)

    c.setFillColor(BLANC)
    c.setFont(FONT_BOLD, 7)

    position_x = x

    for i, entete in enumerate(entetes):
        c.drawString(position_x + 5, y + hauteur_ligne / 2 - 2, str(entete))
        position_x += largeur_colonnes[i]

    position_y = y - hauteur_ligne

    for ligne in lignes:
        c.setFillColor(GRIS_FOND)
        c.rect(x, position_y, largeur_totale, hauteur_ligne, fill=1, stroke=0)

        c.setStrokeColor(GRIS_LIGNE)
        c.rect(x, position_y, largeur_totale, hauteur_ligne, fill=0, stroke=1)

        c.setFillColor(BLEU_NUIT)
        c.setFont(FONT_NORMAL, 6.5)

        position_x = x

        for i, cellule in enumerate(ligne):
            texte = str(cellule)

            if len(texte) > 38:
                texte = texte[:35] + "..."

            c.drawString(position_x + 5, position_y + hauteur_ligne / 2 - 2, texte)
            position_x += largeur_colonnes[i]

        position_y -= hauteur_ligne

    return position_y