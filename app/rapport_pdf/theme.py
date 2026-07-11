from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm


PAGE_SIZE = A4
PAGE_WIDTH, PAGE_HEIGHT = A4

MARGIN_X = 1.1 * cm
MARGIN_TOP = 1.0 * cm
MARGIN_BOTTOM = 1.0 * cm

BLEU_NUIT = HexColor("#0F172A")
BLEU = HexColor("#1D4ED8")
BLEU_2 = HexColor("#2563EB")
BLEU_CLAIR = HexColor("#EFF6FF")

GRIS_FOND = HexColor("#F8FAFC")
GRIS_LIGNE = HexColor("#CBD5E1")
GRIS_TEXTE = HexColor("#475569")
GRIS_CLAIR = HexColor("#E2E8F0")

VERT = HexColor("#16A34A")
ORANGE = HexColor("#F59E0B")
ROUGE = HexColor("#DC2626")
JAUNE = HexColor("#FACC15")

BLANC = colors.white
NOIR = colors.black

FONT_NORMAL = "Helvetica"
FONT_BOLD = "Helvetica-Bold"


def couleur_score(score):
    if score >= 80:
        return VERT
    elif score >= 50:
        return ORANGE
    return ROUGE


def couleur_alerte(niveau):
    if niveau == "Critique":
        return ROUGE
    elif niveau == "Élevé":
        return ORANGE
    elif niveau == "Moyen":
        return JAUNE
    return BLEU