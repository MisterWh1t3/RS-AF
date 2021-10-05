#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import datetime
import requests
from bs4 import BeautifulSoup
from modulos import archivos

def domain_scan(verbose, addr_up):
    domain_found = []
    url = "https://securitytrails.com/list/ip/"
    tiempoInicio = datetime.now()
    for ip in addr_up:
        
        if verbose:
            print(f"\nBuscando dominios con la IP: {ip}")
        try:
            re = requests.get(url+ip)
        except:
            print("[Error] - Problema con la conexión a Internet.")
            continue

        try:
            soup = BeautifulSoup(re.text, "lxml")
        except:
            soup = BeautifulSoup(re.text, "html.parser")
        
        resultado = soup.findAll("a", class_="link-new-ui")  # Cambió un parámetro en Security-Trails
        resultado = soup.findAll("a", class_="link")
        for domain in resultado:
            if domain not in domain_found:
                domain_found.append(domain.get_text())
        
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
    resultados = {}
    dominios = archivos.open_file(verbose, filename, cont)
    for dominio in dominios:
        if verbose:
            print(f"\nBuscando patrón en el dominio: {dominio}")
        try:
            re = requests.get("http://" + dominio)
        except:
            print(f"[Error] - No se ha podido conectar al dominio {dominio}.")
            continue
        
        try:
            soup = BeautifulSoup(re.text, "lxml")
        except:
            soup = BeautifulSoup(re.text, "html.parser")
        
        # Buscar en TITLE
        if soup.find('title') != None and kit.lower() in soup.find('title').get_text().lower():
            title = soup.find('title').get_text()
            if verbose:
                print(f"El patrón fue encontrado en el Título: \n{title}\n")
        else:
            title = None
        
        # Buscar en Description
        metas = soup.findAll('meta')
        desc = None
        for meta in metas:
            if meta.get('name') == 'description':
                if kit.lower() in meta.get('content').lower():
                    desc = meta.get('content')
                    if verbose:
                        print(f"El patrón fue encontrado en la descripción:\n {desc}\n")
            else:
                desc = None
        
        # Buscar en PATH
        path = []
        links =  [i.get('src') for i in soup.findAll('img')]\
                  + [i.get('href') for i in soup.findAll('a')]\
                  + [i.get('href') for i in soup.findAll('link')]\
                  + [re.url]
        
        ## Eliminando los path vacios
        links = list(filter(None, links))
        
        for link in links:
            if kit.lower() in link.lower():
                path.append(link)
                if verbose:
                    print(f"El patrón fue encontrado en el path: \n{link}\n")

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
