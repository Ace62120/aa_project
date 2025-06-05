#!/usr/bin/env python3
# AA Project - version 1.0.0

import socket
import zipfile
from termcolor import cprint
from datetime import datetime

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
def scan_ports(target, ports=[21, 22, 80, 443, 8080]):
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
    return False

# -------- Main --------
if __name__ == "__main__":
    show_banner()

    # Exemples à modifier selon ton test :
    scan_ports("127.0.0.1")

    # Brute-force (exemple)
    # crack_zip("secret.zip", "wordlist.txt")
