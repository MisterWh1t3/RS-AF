#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import platform
from datetime import datetime

# Definir el comando ping según el tipo de OS.
if (platform.system()=="Windows"):
    ping = "ping -n 1"
else:
    ping = "ping -c 1"

def ip_scan(verbose, force, red, comienzo, fin):
    addr_up = []
    if force:
        for subnet in range(comienzo, fin+1):
            direccion = red + str(subnet)
            addr_up.append(direccion)
        return addr_up
    
    tiempoInicio = datetime.now()
    print("\n[*] El escaneo se está realizando desde",red+str(comienzo),"hasta",red+str(fin))
    for subnet in range(comienzo, fin+1):
        direccion = red + str(subnet)
        response = os.popen(ping+" "+direccion).read(200)
        if "ttl" in response.lower():
            addr_up.append(direccion)
            if verbose:
                print(direccion,"está activo")
        else:
            if verbose:
                print(direccion, "está caido")

    tiempoFinal = datetime.now()
    tiempo = tiempoFinal - tiempoInicio
    print(f"[*] El escaneo de IPs ha durado {tiempo}")
    if verbose:
        print(f"Se detectaron las siguientes IP activas:\n{', '.join(addr_up)}")
    return addr_up

def IPrange_scan(verbose, force, red):
    addr_up = []
    if force:
        for ip in red:
            addr_up.append(str(ip))
        return addr_up

    tiempoInicio = datetime.now()
    print(f"\n[*] Escaneando el rango IP {red}")
    for ip in red:
        ip = str(ip)
        response = os.popen(ping+" "+ip).read(200)
        if "ttl" in response.lower():
            addr_up.append(ip)
            if verbose:
                print(ip,"está activo")
        else:
            if verbose:
                print(ip, "está caido")

    tiempoFinal = datetime.now()
    tiempo = tiempoFinal - tiempoInicio
    print(f"[*] El escaneo de IPs ha durado {tiempo}")
    if verbose:
        print(f"\nSe detectaron las siguientes IP activas:\n{', '.join(addr_up)}")
    return addr_up
