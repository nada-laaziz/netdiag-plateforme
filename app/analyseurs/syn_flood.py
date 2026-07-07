def analyser_syn_flood(paquets):
    """
    Détecte un possible SYN Flood en comparant le nombre
    de paquets SYN et ACK.
    """

    syn = 0
    ack = 0

    for paquet in paquets:

        if not paquet.haslayer("TCP"):
            continue

        flags = paquet["TCP"].flags

        # SYN seul
        if flags == 0x02:
            syn += 1

        # ACK (ACK ou SYN+ACK)
        if flags & 0x10:
            ack += 1

    resultat = {
        "syn": syn,
        "ack": ack,
        "suspect": False
    }

    if syn > 100 and syn > (ack * 2):
        resultat["suspect"] = True

    return resultat