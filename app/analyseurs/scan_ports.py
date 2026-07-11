def analyser_scan_ports(resultats, seuil_ports=10):
    scans = []

    ports_par_ip = resultats.get("ports_par_ip", {})

    for ip, ports in ports_par_ip.items():
        nombre_ports = len(ports)

        if nombre_ports >= seuil_ports:
            scans.append({
                "ip": ip,
                "nombre_ports": nombre_ports,
                "ports": sorted(list(ports)),
                "suspect": True
            })

    return scans