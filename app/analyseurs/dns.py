from scapy.layers.dns import DNS, DNSQR


def analyser_dns(paquets):
    total_dns = 0
    requetes_dns = 0
    domaines = {}

    for paquet in paquets:
        if paquet.haslayer(DNS):
            total_dns += 1

            if paquet.haslayer(DNSQR):
                requetes_dns += 1
                domaine = paquet[DNSQR].qname.decode(errors="ignore").rstrip(".")

                domaines[domaine] = domaines.get(domaine, 0) + 1

    domaines_tries = sorted(domaines.items(), key=lambda x: x[1], reverse=True)

    return {
        "total_dns": total_dns,
        "requetes_dns": requetes_dns,
        "top_domaines": domaines_tries[:5]
    }