def analyser_top_talkers(resultats, seuil=20):
    """
    Détecte les IP qui représentent au moins 'seuil' % du trafic.
    """

    top_talkers = []

    total = resultats["nombre_paquets"]

    if total == 0:
        return top_talkers

    for ip, nb_paquets in resultats["ip_sources"].items():
        pourcentage = (nb_paquets / total) * 100

        if pourcentage >= seuil:
            top_talkers.append({
                "ip": ip,
                "paquets": nb_paquets,
                "pourcentage": round(pourcentage, 2)
            })

    return top_talkers