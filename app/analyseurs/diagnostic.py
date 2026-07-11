def generer_diagnostic_final(resultats):
    alertes = resultats.get("alertes", [])

    nb_moyen = 0
    nb_eleve = 0
    nb_critique = 0

    score = 100

    for alerte in alertes:
        niveau = alerte.get("niveau", "")

        if niveau == "Moyen":
            nb_moyen += 1
            score -= 5

        elif niveau == "Élevé":
            nb_eleve += 1
            score -= 15

        elif niveau == "Critique":
            nb_critique += 1
            score -= 30

    if score < 0:
        score = 0

    if score >= 90:
        statut = "Excellent"
        message = "Le réseau présente très peu d'anomalies."

    elif score >= 75:
        statut = "Bon"
        message = "Le réseau est globalement sain mais quelques points doivent être surveillés."

    elif score >= 50:
        statut = "À surveiller"
        message = "Plusieurs anomalies ont été détectées."

    else:
        statut = "Critique"
        message = "Le réseau présente plusieurs anomalies importantes nécessitant une analyse."

    return {
        "score": score,
        "statut": statut,
        "message": message,
        "alertes_moyennes": nb_moyen,
        "alertes_elevees": nb_eleve,
        "alertes_critiques": nb_critique
    }