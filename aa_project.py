#!/usr/bin/env python3
# AA Project - version 1.0.0

import socket
import zipfile
from termcolor import cprint
from datetime import datetime
import os
import itertools
import string

# -------- Banner --------
def show_banner():
    cprint(r"""
 █████╗  █████╗       ██████╗ ██████╗       ██████╗ ██████╗
██╔══██╗██╔══██╗     ██╔═══██╗██╔══██╗     ██╔════╝██╔═══██╗
███████║███████║     ██║   ██║██████╔╝     ██║     ██║   ██║
██╔══██║██╔══██║     ██║   ██║██╔═══╝      ██║     ██║   ██║
██║  ██║██║  ██║     ╚██████╔╝██║          ╚██████╗╚██████╔╝
╚═╝  ╚═╝╚═╝  ╚═╝      ╚═════╝ ╚═╝           ╚═════╝ ╚═════╝

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

# -------- ZIP Brute Force (Wordlist) --------
def crack_zip(zip_path, wordlist_path):
    print(f"\n[+] Attempting to crack ZIP file with wordlist: {zip_path}")
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

# -------- ZIP Brute Force (Exhaustive) --------
def crack_zip_exhaustive(zip_path, max_length=4):
    print(f"\n[+] Bruteforce total (max {max_length} caractères)...")
    chars = string.ascii_letters + string.digits

    try:
        with zipfile.ZipFile(zip_path) as zf:
            for length in range(1, max_length + 1):
                for pwd_tuple in itertools.product(chars, repeat=length):
                    password = ''.join(pwd_tuple)
                    try:
                        zf.extractall(pwd=bytes(password, 'utf-8'))
                        cprint(f"[+] Mot de passe trouvé : {password}", "red")
                        return True
                    except:
                        continue
        print("[-] Mot de passe non trouvé.")
    except FileNotFoundError:
        print("[-] Fichier ZIP introuvable.")
    return False

# -------- Générer un ZIP protégé --------
def create_protected_zip():
    try:
        import pyminizip
    except ImportError:
        print("[-] Le module 'pyminizip' est requis. Installe-le avec : pip install pyminizip")
        return

    file_path = input("Chemin du fichier à zipper : ")
    if not os.path.isfile(file_path):
        print("[-] Fichier introuvable.")
        return

    zip_name = input("Nom du fichier ZIP de sortie : ")
    password = input("Mot de passe : ")

    try:
        pyminizip.compress(file_path, None, zip_name, password, 5)
        cprint(f"[+] ZIP protégé créé : {zip_name}", "red")
    except Exception as e:
        print(f"[-] Erreur : {e}")

# -------- Menu Interface --------
def main():
    show_banner()
    while True:
        print("\nMenu:")
        print("1. Scanner des ports")
        print("2. Bruteforce de fichier ZIP")
        print("3. Générer un ZIP protégé par mot de passe")
        print("4. Quitter")
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
            mode = input("Mode (1: wordlist / 2: bruteforce total): ")
            if mode == '1':
                wordlist_path = input("Chemin vers la wordlist: ")
                crack_zip(zip_path, wordlist_path)
            elif mode == '2':
                max_len = int(input("Longueur max du mot de passe (ex: 4): "))
                crack_zip_exhaustive(zip_path, max_len)

        elif choice == '3':
            create_protected_zip()

        elif choice == '4':
            print("Au revoir.")
            break
        else:
            print("Option invalide, réessaye.")

if __name__ == "__main__":
    main()
