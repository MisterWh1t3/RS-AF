#!/usr/bin/python3
# -*- coding: utf-8 -*-

from requests_html import HTMLSession
from datetime import datetime
from modulos import archivos

session = HTMLSession()

def domain_scan(verbose, addr_up):
    domain_found = []
    url = "https://securitytrails.com/list/ip/"
    tiempoInicio = datetime.now()
    for ip in addr_up:
        
        if verbose:
            print(f"\nBuscando dominios con la IP: {ip}")
        try:
            r = session.get(url+ip)
        except:
            print("[Error] - Problema con la conexión a Internet.")
            continue
        
        #resultado = r.html.find('a.link-new-ui')
        resultado = r.html.find('a.link')

        #print(f"resulrados: {resultado}")
        for domain in resultado:
            if domain not in domain_found:
                domain_found.append(domain.full_text)
        
    if verbose:
        if domain_found:
            print(f"Dominios encontrados: {', '.join(domain_found)}")
        else:
            print(f"No se encontraron dominios para la IP {ip}")
        
    if domain_found:
        filename = archivos.save_domain(verbose, domain_found)
    else:
        print("No se encontraron dominios.  :(")
        exit()
    
    tiempoFinal = datetime.now()
    tiempo = tiempoFinal - tiempoInicio
    print(f"[*] El escaneo de dominio ha durado {tiempo}")
    return filename

def kit_scan(verbose, filename, kit, cont):
    num = 0
    resultados = {}
    dominios = archivos.open_file(verbose, filename, cont)
    num_dom = len(dominios)
    for dominio in dominios:
        num += 1
        if verbose:
            print(f"\n[{num}/{num_dom}] - Buscando patrón en el dominio: {dominio}")
        try:
            r = session.get("http://" + dominio)
        except:
            print(f"[Error] - No se ha podido conectar al dominio {dominio}")
            continue
        
        # Buscar en TITLE
        title = r.html.find('title', first=True)
        if title and kit.lower() in title.full_text.lower():
            title = title.full_text
            if verbose:
                print(f"El patrón fue encontrado en el Título:\n {title}\n")
        else:
            title = None
        
        # Buscar en Description
        desc = r.html.xpath('//meta[@name="description"]/@content', first=True)
        if desc and kit.lower() in desc.lower():
            if verbose:
                print(f"El patrón fue encontrado en la descripción:\n {desc}\n")
        else:
            desc = None
        
        # Buscar en PATH
        path = []
        links = r.html.absolute_links
        
        for link in links:
            if kit.lower() in link.lower():
                path.append(link)
                if verbose:
                    print(f"El patrón fue encontrado en el path:\n{link}\n")

        if title or desc or path:
            resultados[dominio] = {}
            if title:
                resultados[dominio]['Title'] = title
            if desc:
                resultados[dominio]['desc'] = desc
            if path:
                resultados[dominio]['path'] = path
    
    if resultados:
        archivos.save_kit(verbose, kit, resultados)
    else:
        print("No se encontró el patrón en ningún dominio.")
