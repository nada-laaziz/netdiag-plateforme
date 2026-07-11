from scapy.layers.inet import IP


def analyser_conversations(paquets):
    conversations = {}

    for paquet in paquets:
        if paquet.haslayer(IP):
            ip_source = paquet[IP].src
            ip_destination = paquet[IP].dst

            paire = tuple(sorted([ip_source, ip_destination]))

            if paire not in conversations:
                conversations[paire] = 0

            conversations[paire] += 1

    conversations_triees = sorted(
        conversations.items(),
        key=lambda x: x[1],
        reverse=True
    )

    top_conversations = []

    for paire, nombre in conversations_triees[:5]:
        top_conversations.append({
            "ip_1": paire[0],
            "ip_2": paire[1],
            "paquets": nombre
        })

    return top_conversations