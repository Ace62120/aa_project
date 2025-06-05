#!/usr/bin/env python3
# AA Project - version 1.0.0

import socket
import zipfile
from termcolor import cprint
from datetime import datetime
import os

# -------- Banner --------
def show_banner():
    cprint(r"""
     █████╗  █████╗     ██████╗  ██████╗      ██████╗ ██████╗      
    ██╔══██╗██╔══██╗    ██╔══██╗██╔═══██╗    ██╔════╝██╔═══██╗     
    ███████║███████║    ██████╔╝██║   ██║    ██║     ██║   ██║     
    ██╔══██║██╔══██║    ██╔═══╝ ██║   ██║    ██║     ██║   ██║     
    ██║  ██║██║  ██║    ██║     ╚██████╔╝    ╚██████╗╚██████╔╝     
    ╚═╝  ╚═╝╚═╝  ╚═╝    ╚═╝      ╚═════╝      ╚═════╝ ╚═════╝      
                Version 1.0.0 | Port Scanner + Zip Cracker
    """, 'red')

# -------- Port Scanner --------
def scan_ports(target, ports):
    print(f"\n[+] Scanning {target} ...\n")
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target, port))
            if result == 0:
                cprint(f"[+] Port {port} is OPEN", "red")
            sock.close()
        except Exception as e:
            print(f"[-] Error on port {port}: {e}")

# -------- ZIP Brute Force --------
def crack_zip(zip_path, wordlist_path):
    print(f"\n[+] Attempting to crack ZIP file: {zip_path}")
    try:
        with zipfile.ZipFile(zip_path) as zf:
            with open(wordlist_path, 'rb') as f:
                for line in f:
                    password = line.strip()
                    try:
                        zf.extractall(pwd=password)
                        cprint(f"[+] Password found: {password.decode()}", "red")
                        return True
                    except:
                        pass
        print("[-] Password not found.")
    except FileNotFoundError:
        print("[-] ZIP file or wordlist not found.")
    return False

# -------- Menu Interface --------
def main():
    show_banner()
    while True:
        print("\nMenu:")
        print("1. Scanner des ports")
        print("2. Bruteforce de fichier ZIP")
        print("3. Quitter")
        choice = input("\n[?] Choix: ")

        if choice == '1':
            target = input("Entrer l'adresse IP ou le nom d'hôte à scanner: ")
            port_input = input("Entrer les ports à scanner (ex: 22,80,443) ou laisser vide pour les ports par défaut: ")
            if port_input.strip():
                ports = list(map(int, port_input.split(',')))
            else:
                ports = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 8080]
            scan_ports(target, ports)

        elif choice == '2':
            zip_path = input("Chemin vers le fichier ZIP: ")
            wordlist_path = input("Chemin vers la wordlist: ")
            crack_zip(zip_path, wordlist_path)

        elif choice == '3':
            print("Au revoir.")
            break
        else:
            print("Option invalide, réessaye.")

if __name__ == "__main__":
    main()
