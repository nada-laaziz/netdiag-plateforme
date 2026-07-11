def generer_alertes(resultats):
    alertes = []

    nombre_paquets = resultats.get("nombre_paquets", 0)
    protocoles = resultats.get("protocoles", {})
    ip_sources = resultats.get("ip_sources", {})
    ip_destinations = resultats.get("ip_destinations", {})
    destinations_par_ip = resultats.get("destinations_par_ip", {})
    syn_flood = resultats.get("syn_flood", {})
    dns = resultats.get("dns", {})
    icmp = resultats.get("icmp", {})
    scan_ports = resultats.get("scan_ports", [])
    top_conversations = resultats.get("top_conversations", [])

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

    if syn_flood.get("suspect"):
        alertes.append({
            "niveau": "Critique",
            "titre": "Possible attaque SYN Flood",
            "description": (
                f"{syn_flood.get('syn', 0)} paquets SYN détectés contre "
                f"{syn_flood.get('ack', 0)} paquets ACK."
            )
        })

    if scan_ports:
        for scan in scan_ports:
            alertes.append({
                "niveau": "Élevé",
                "titre": "Possible scan de ports",
                "description": (
                    f"L'adresse IP {scan['ip']} a contacté "
                    f"{scan['nombre_ports']} ports différents."
                )
            })

    total_dns = dns.get("total_dns", 0)

    if total_dns > nombre_paquets * 0.30:
        alertes.append({
            "niveau": "Moyen",
            "titre": "Trafic DNS important",
            "description": (
                f"{total_dns} paquets DNS détectés. "
                "Un volume DNS élevé peut indiquer beaucoup de navigation, "
                "des requêtes répétées ou une activité inhabituelle."
            )
        })

    total_icmp = icmp.get("total_icmp", 0)

    if total_icmp > nombre_paquets * 0.20:
        alertes.append({
            "niveau": "Moyen",
            "titre": "Trafic ICMP important",
            "description": (
                f"{total_icmp} paquets ICMP détectés. "
                "Cela peut indiquer un test réseau, un scan ou un problème de connectivité."
            )
        })

    for ip, destinations in destinations_par_ip.items():
        if len(destinations) >= 20:
            alertes.append({
                "niveau": "Élevé",
                "titre": "Communication avec beaucoup de machines",
                "description": f"L'adresse IP {ip} a communiqué avec {len(destinations)} adresses IP différentes."
            })

    for conversation in top_conversations:
        pourcentage = (conversation["paquets"] / nombre_paquets) * 100

        if pourcentage > 40:
            alertes.append({
                "niveau": "Moyen",
                "titre": "Conversation réseau dominante",
                "description": (
                    f"La communication entre {conversation['ip_1']} et "
                    f"{conversation['ip_2']} représente {pourcentage:.2f}% du trafic."
                )
            })

    return alertes