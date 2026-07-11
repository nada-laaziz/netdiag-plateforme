from scapy.layers.inet import IP, ICMP


def analyser_icmp(paquets):
    total_icmp = 0
    sources_icmp = {}

    for paquet in paquets:
        if paquet.haslayer(IP) and paquet.haslayer(ICMP):
            total_icmp += 1
            ip_source = paquet[IP].src

            sources_icmp[ip_source] = sources_icmp.get(ip_source, 0) + 1

    sources_tries = sorted(sources_icmp.items(), key=lambda x: x[1], reverse=True)

    return {
        "total_icmp": total_icmp,
        "top_sources_icmp": sources_tries[:5]
    }