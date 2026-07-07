def generer_alertes(resultats):
    alertes = []

    nombre_paquets = resultats["nombre_paquets"]
    protocoles = resultats["protocoles"]
    ip_sources = resultats["ip_sources"]
    ip_destinations = resultats["ip_destinations"]
    ports_par_ip = resultats.get("ports_par_ip", {})
    destinations_par_ip = resultats.get("destinations_par_ip", {})
    syn_flood = resultats.get("syn_flood", {})

    if nombre_paquets == 0:
        return alertes

    if protocoles.get("HTTP", 0) > 0:
        alertes.append({
            "niveau": "Moyen",
            "titre": "Trafic HTTP détecté",
            "description": "Certaines communications ne sont pas chiffrées. HTTPS est recommandé."
        })

    if protocoles.get("TELNET", 0) > 0:
        alertes.append({
            "niveau": "Élevé",
            "titre": "Utilisation de TELNET",
            "description": "TELNET transmet les données sans chiffrement. Il est recommandé d'utiliser SSH."
        })

    services_sensibles = ["FTP", "TELNET", "SMB", "RDP"]

    for service in services_sensibles:
        if protocoles.get(service, 0) > 0:
            alertes.append({
                "niveau": "Élevé",
                "titre": f"Service sensible détecté : {service}",
                "description": f"Le service {service} peut représenter un risque s'il est exposé ou mal configuré."
            })

    for ip, total in ip_sources.items():
        pourcentage = (total / nombre_paquets) * 100

        if pourcentage > 50:
            alertes.append({
                "niveau": "Moyen",
                "titre": "IP source très active",
                "description": f"L'adresse IP {ip} génère {pourcentage:.2f}% du trafic total."
            })

    for ip, total in ip_destinations.items():
        pourcentage = (total / nombre_paquets) * 100

        if pourcentage > 50:
            alertes.append({
                "niveau": "Moyen",
                "titre": "IP destination très sollicitée",
                "description": f"L'adresse IP {ip} reçoit {pourcentage:.2f}% du trafic total."
            })

    if protocoles.get("ICMP", 0) > nombre_paquets * 0.20:
        alertes.append({
            "niveau": "Moyen",
            "titre": "Trafic ICMP important",
            "description": "Beaucoup de paquets ICMP peuvent indiquer un scan, un test réseau ou un problème de connectivité."
        })

    for ip, ports in ports_par_ip.items():
        if len(ports) >= 20:
            alertes.append({
                "niveau": "Élevé",
                "titre": "Possible scan de ports",
                "description": f"L'adresse IP {ip} a tenté d'accéder à {len(ports)} ports différents."
            })

    for ip, destinations in destinations_par_ip.items():
        if len(destinations) >= 20:
            alertes.append({
                "niveau": "Élevé",
                "titre": "Communication avec beaucoup de machines",
                "description": f"L'adresse IP {ip} a communiqué avec {len(destinations)} adresses IP différentes."
            })

    if syn_flood.get("suspect"):
        alertes.append({
            "niveau": "Critique",
            "titre": "Possible attaque SYN Flood",
            "description": (
                f"{syn_flood.get('syn', 0)} paquets SYN détectés contre "
                f"{syn_flood.get('ack', 0)} paquets ACK."
            )
        })

    return alertes