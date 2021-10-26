#!/usr/bin/python3
# -*- coding: utf-8 -*-


import argparse
import ipaddress
import json
from modulos import scan, search
from modulos.archivos import open_file

def parse_args():
    parser = argparse.ArgumentParser(description="Herramienta para el Departamento de AntiFraude - Hispasec ")
    parser.add_argument("-v", "--verbose", action="store_true", help="Ver detalles del proceso.")
    parser.add_argument("-o", "--open", metavar="File", type=str, help="Abrir y visualizar archivo contenedor de patrones encontrados.")
    parser.add_argument("-f", "--force", action="store_true", help="No realizar prueba de conectividad.")
    parser.add_argument("-a", "--archive", metavar="File", type=str, help="Archivo contenedor de dominios.")
    parser.add_argument("-r", "--range", metavar='Range', type=str, help="Rango IP a escanear. Ej: 192.168.1.1/24.")
    args = parser.parse_args()
    return args

def main(args):
    # Visualizar los patrones guardados
    if args.open:
        kits = json.loads(open_file(args.verbose, args.open, False)[0])
        for key in kits.keys():
            print("\n" + "-"*50)
            print(f"Dominio: {key}")
            print("-"*50)
            for i in kits[key]:
                print(f"Patrón en: {i}\n    {kits[key][i]}")
        print()
        search.search_quit()
        exit()

    # Si se parte desde un histórico
    if args.archive:
        kit = input("Ingrese el patrón a buscar: ")
        search.kit_scan(args.verbose, args.archive, kit, False)
        search.search_quit()
        exit()
    
    # Buscar las IP activas
    if args.range:
        try:
            red = ipaddress.ip_network(args.range, False)
        except:
            print(f"[Error] - {args.range} no es un rango valido...")
            search.search_quit()
            exit(1)
        
        addr_up = scan.IPrange_scan(args.verbose, args.force, red)

    else:
        ip = input("Ingresa la dirección IP de la red: ")
        try:
            ipaddress.ip_address(ip)
        except:
            print(f"[Error] - {ip} no es una dirección IP valida.")
            search.search_quit()
            exit(1)

        ipDividida = ip.split('.')
        red = ipDividida[0]+'.'+ipDividida[1]+'.'+ipDividida[2]+'.'
        while True:
            try:
                comienzo = int(input("Ingresa el número de comienzo de la subred: "))
                fin = int(input("Ingresa el número en el que deseas acabar el barrido: "))
                break
            except:
                print("[Error] - No se ingresó correctamente los valores. Recuerde que tienen que ser números enteros.")

        addr_up = scan.ip_scan(args.verbose, args.force, red, comienzo, fin)

    # Buscar los dominios
    if addr_up:
        filename = search.domain_scan(args.verbose, addr_up)
    else:
        print("No se encontraron IP activas.  :(")
        search.search_quit()
        exit(1)
    
    # Buscar patrones en los dominios encontrados
    patron = input("¿Continuar con la busqueda de patrones? [y/N]: ").lower()
    if patron == 'y':
        kit = input("Ingrese el patrón a buscar: ")
        search.kit_scan(args.verbose, filename, kit, True)
    else:
        search.search_quit()
        exit()
    
    search.search_quit()


if __name__ == '__main__':
    args = parse_args()
    main(args)
