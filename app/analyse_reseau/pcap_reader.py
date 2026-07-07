from scapy.all import rdpcap
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.l2 import ARP

from .protocoles import service_depuis_port
from .regles_diagnostic import generer_alertes
from app.analyseurs.syn_flood import analyser_syn_flood


def analyser_pcap(chemin_fichier):
    paquets = rdpcap(chemin_fichier)

    protocoles = {
        "HTTP": 0,
        "HTTPS": 0,
        "DNS": 0,
        "DHCP": 0,
        "FTP": 0,
        "SSH": 0,
        "TELNET": 0,
        "SMTP": 0,
        "POP3": 0,
        "IMAP": 0,
        "NTP": 0,
        "SNMP": 0,
        "TFTP": 0,
        "LDAP": 0,
        "SMB": 0,
        "MySQL": 0,
        "RDP": 0,
        "PostgreSQL": 0,
        "TCP": 0,
        "UDP": 0,
        "ICMP": 0,
        "ARP": 0,
        "Autres": 0
    }

    ip_sources = {}
    ip_destinations = {}
    services = {}
    communications = []
    ports_par_ip = {}
    destinations_par_ip = {}

    syn_flood = analyser_syn_flood(paquets)

    for paquet in paquets:
        service = "Inconnu"

        if paquet.haslayer(IP):
            ip_source = paquet[IP].src
            ip_destination = paquet[IP].dst

            ip_sources[ip_source] = ip_sources.get(ip_source, 0) + 1
            ip_destinations[ip_destination] = ip_destinations.get(ip_destination, 0) + 1

            if ip_source not in destinations_par_ip:
                destinations_par_ip[ip_source] = set()
            destinations_par_ip[ip_source].add(ip_destination)

            if paquet.haslayer(TCP):
                sport = paquet[TCP].sport
                dport = paquet[TCP].dport

                if ip_source not in ports_par_ip:
                    ports_par_ip[ip_source] = set()
                ports_par_ip[ip_source].add(dport)

                service_source = service_depuis_port(sport)
                service_destination = service_depuis_port(dport)

                if service_destination != "Inconnu":
                    service = service_destination
                elif service_source != "Inconnu":
                    service = service_source
                else:
                    service = "TCP"

                if service in protocoles:
                    protocoles[service] += 1
                else:
                    protocoles["TCP"] += 1

            elif paquet.haslayer(UDP):
                sport = paquet[UDP].sport
                dport = paquet[UDP].dport

                service_source = service_depuis_port(sport)
                service_destination = service_depuis_port(dport)

                if service_destination != "Inconnu":
                    service = service_destination
                elif service_source != "Inconnu":
                    service = service_source
                else:
                    service = "UDP"

                if service in protocoles:
                    protocoles[service] += 1
                else:
                    protocoles["UDP"] += 1

            elif paquet.haslayer(ICMP):
                service = "ICMP"
                protocoles["ICMP"] += 1

            else:
                protocoles["Autres"] += 1

            services[service] = services.get(service, 0) + 1

            communications.append({
                "ip_source": ip_source,
                "ip_destination": ip_destination,
                "service": service
            })

        elif paquet.haslayer(ARP):
            protocoles["ARP"] += 1
            services["ARP"] = services.get("ARP", 0) + 1

        else:
            protocoles["Autres"] += 1

    resultats = {
        "nombre_paquets": len(paquets),
        "protocoles": protocoles,
        "ip_sources": ip_sources,
        "ip_destinations": ip_destinations,
        "services": services,
        "communications": communications,
        "ports_par_ip": ports_par_ip,
        "destinations_par_ip": destinations_par_ip,
        "syn_flood": syn_flood
    }

    resultats["alertes"] = generer_alertes(resultats)

    return resultats