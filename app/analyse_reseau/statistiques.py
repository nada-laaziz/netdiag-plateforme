def generer_statistiques(resultats):

    statistiques = {}

    statistiques["nombre_paquets"] = resultats["nombre_paquets"]

    statistiques["nombre_ip_sources"] = len(resultats["ip_sources"])
    statistiques["nombre_ip_destinations"] = len(resultats["ip_destinations"])

    protocole_dominant = max(
        resultats["protocoles"],
        key=resultats["protocoles"].get
    )

    statistiques["protocole_dominant"] = protocole_dominant

    if resultats["ip_sources"]:
        ip_source_dominante = max(
            resultats["ip_sources"],
            key=resultats["ip_sources"].get
        )

        statistiques["ip_source_dominante"] = ip_source_dominante
        statistiques["paquets_ip_source"] = resultats["ip_sources"][ip_source_dominante]

    if resultats["ip_destinations"]:
        ip_destination_dominante = max(
            resultats["ip_destinations"],
            key=resultats["ip_destinations"].get
        )

        statistiques["ip_destination_dominante"] = ip_destination_dominante
        statistiques["paquets_ip_destination"] = resultats["ip_destinations"][ip_destination_dominante]

    return statistiques