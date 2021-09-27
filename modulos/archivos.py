#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import datetime
import json
import os, os.path

fecha = datetime.today().strftime ("%y%m%d")
folder = "resultados"
if not os.path.exists(folder):
         os.mkdir(folder)

def save_domain(verbose, domain_found):
    file_name = "dominios-" + fecha + ".txt"
    with open(os.path.join(folder, file_name), "w") as fichero:
        for line in domain_found:
            fichero.write(line + "\n")
    
    print(f"\nLos dominios han sido guardados en el fichero {file_name}\n")
    return file_name

def open_file(verbose, file_name, cont = False):
    if cont:
        with open(os.path.join(folder, "dominios-" + fecha + ".txt"), 'r') as fichero:
            dominio = fichero.read().splitlines()
    else:
        if os.path.exists(file_name):
            with open(file_name, 'r') as fichero:
                dominio = fichero.read().splitlines()
        else:
            print(f"El fichero '{file_name}' no existe.  :(")
            exit(1)
    
    return dominio

def save_kit(verbose, kit, resultados):
    file_name = kit + "-" + fecha + ".json"
    with open(os.path.join(folder, file_name), "w") as fichero:
        json.dump(resultados ,fichero)
    
    print(f"\nLos dominios han sido guardados en el fichero {file_name}\n")
