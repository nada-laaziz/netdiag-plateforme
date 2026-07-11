from app.analyse_reseau.pcap_reader import analyser_pcap
from app.analyse_reseau.statistiques import generer_statistiques
from app.analyse_reseau.top_talkers import analyser_top_talkers


resultat = analyser_pcap("test.pcapng")

statistiques = generer_statistiques(resultat)
top_talkers = analyser_top_talkers(resultat)


print("=" * 60)
print("RAPPORT D'ANALYSE NETDIAG")
print("=" * 60)

print("\nSTATISTIQUES GÉNÉRALES")
print(f"Nombre de paquets : {statistiques['nombre_paquets']}")
print(f"Nombre d'IP sources : {statistiques['nombre_ip_sources']}")
print(f"Nombre d'IP destinations : {statistiques['nombre_ip_destinations']}")
print(f"Protocole dominant : {statistiques['protocole_dominant']}")

if "ip_source_dominante" in statistiques:
    print(
        f"IP source dominante : {statistiques['ip_source_dominante']} "
        f"({statistiques['paquets_ip_source']} paquets)"
    )

if "ip_destination_dominante" in statistiques:
    print(
        f"IP destination dominante : {statistiques['ip_destination_dominante']} "
        f"({statistiques['paquets_ip_destination']} paquets)"
    )

print("\nPROTOCOLES DÉTECTÉS")
for protocole, nombre in resultat["protocoles"].items():
    if nombre > 0:
        print(f"{protocole} : {nombre}")

print("\nTOP 5 IP SOURCES")
top_sources = sorted(
    resultat["ip_sources"].items(),
    key=lambda x: x[1],
    reverse=True
)[:5]

for ip, nombre in top_sources:
    print(f"{ip} : {nombre}")

print("\nTOP 5 IP DESTINATIONS")
top_destinations = sorted(
    resultat["ip_destinations"].items(),
    key=lambda x: x[1],
    reverse=True
)[:5]

for ip, nombre in top_destinations:
    print(f"{ip} : {nombre}")

print("\nTOP TALKERS")

if top_talkers:
    for machine in top_talkers:
        print(
            f"{machine['ip']} : "
            f"{machine['paquets']} paquets "
            f"({machine['pourcentage']} %)"
        )
else:
    print("Aucun Top Talker détecté.")


print("\nTOP COMMUNICATIONS")

destinations_par_ip = resultat.get("destinations_par_ip", {})

top_communications = sorted(
    destinations_par_ip.items(),
    key=lambda x: len(x[1]),
    reverse=True
)[:5]

if top_communications:
    for ip, destinations in top_communications:
        print(f"{ip} : {len(destinations)} machines différentes contactées")
else:
    print("Aucune communication détectée.")
print("\nSYN FLOOD")

syn_flood = resultat.get("syn_flood", {})

if syn_flood:
    print(f"Paquets SYN : {syn_flood.get('syn', 0)}")
    print(f"Paquets ACK : {syn_flood.get('ack', 0)}")

    if syn_flood.get("suspect"):
        print("Résultat : Possible attaque SYN Flood")
    else:
        print("Résultat : Aucun SYN Flood détecté")
else:
    print("Analyse SYN Flood non disponible.")

print("\nANALYSE DNS")

dns = resultat.get("dns", {})

print(f"Nombre de paquets DNS : {dns.get('total_dns', 0)}")
print(f"Nombre de requêtes DNS : {dns.get('requetes_dns', 0)}")

if dns.get("top_domaines"):
    print("\nTop domaines DNS")
    for domaine, nombre in dns["top_domaines"]:
        print(f"{domaine} : {nombre}")
else:
    print("Aucun domaine DNS détecté.")
print("\nANALYSE ICMP")

icmp = resultat.get("icmp", {})

print(f"Nombre de paquets ICMP : {icmp.get('total_icmp', 0)}")

if icmp.get("top_sources_icmp"):
    print("\nTop sources ICMP")
    for ip, nombre in icmp["top_sources_icmp"]:
        print(f"{ip} : {nombre}")
else:
    print("Aucun trafic ICMP détecté.")

print("\nSCAN DE PORTS")

scan_ports = resultat.get("scan_ports", [])

if scan_ports:
    for scan in scan_ports:
        print(
            f"{scan['ip']} : scan suspect, "
            f"{scan['nombre_ports']} ports contactés"
        )
        print(f"Ports : {scan['ports']}")
else:
    print("Aucun scan de ports suspect détecté.")

print("\nTOP CONVERSATIONS")

top_conversations = resultat.get("top_conversations", [])

if top_conversations:
    for conversation in top_conversations:
        print(
            f"{conversation['ip_1']} <-> {conversation['ip_2']} : "
            f"{conversation['paquets']} paquets"
        )
else:
    print("Aucune conversation détectée.")


print("\nALERTES")

if resultat["alertes"]:
    for alerte in resultat["alertes"]:
        if isinstance(alerte, dict):
            print(f"• [{alerte['niveau']}] {alerte['titre']}")
            print(f"  {alerte['description']}")
        else:
            print(f"• {alerte}")
else:
    print("Aucune alerte détectée.")


print("\nDIAGNOSTIC FINAL")

diagnostic = resultat.get("diagnostic_final", {})

print(f"Score réseau : {diagnostic.get('score', 0)} / 100")
print(f"Statut : {diagnostic.get('statut', 'Non disponible')}")
print(f"Message : {diagnostic.get('message', 'Non disponible')}")
print(f"Alertes moyennes : {diagnostic.get('alertes_moyennes', 0)}")
print(f"Alertes élevées : {diagnostic.get('alertes_elevees', 0)}")
print(f"Alertes critiques : {diagnostic.get('alertes_critiques', 0)}")

from app.rapport_pdf.generer_pdf import generer_pdf

generer_pdf(resultat, "rapport_netdiag.pdf")

print("\nRapport PDF généré avec succès.")