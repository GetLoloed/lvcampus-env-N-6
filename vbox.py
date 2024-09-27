import subprocess
import os
import platform
import requests
from colorama import init, Fore, Style
from urllib.parse import urlparse
import tempfile

def wget(url, output_directory='.'):
    try:
        nom_fichier = os.path.basename(urlparse(url).path)
        if not nom_fichier:
            nom_fichier = 'index.html'
        chemin_fichier = os.path.join(output_directory, nom_fichier)
        print(f"Téléchargement de {url}")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(chemin_fichier, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Fichier sauvegardé sous : {chemin_fichier}")
        return chemin_fichier
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors du téléchargement : {e}")
        return None

def vbox_install():
    print("Menu d'installation de VirtualBox")
    print("1. Créer une nouvelle machine virtuelle")
    print("2. Retour au menu principal")
    
    choix = input("Veuillez entrer votre choix (1 ou 2) : ")
    
    if choix == "1":
        create_virtual_machine()
    elif choix == "2":
        print("Retour au menu principal...")
    else:
        print("Choix invalide. Retour au menu principal...")

def create_virtual_machine():
    print("Création d'une nouvelle machine virtuelle...")
    if platform.system() == "Windows":
        vboxmanage = r"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"
        print("Téléchargement de VirtualBox sur Windows...")
        virtualBoxUrl = "https://download.virtualbox.org/virtualbox/7.0.10/VirtualBox-7.0.10-158379-Win.exe"
        destination = os.path.join(tempfile.gettempdir(), "VirtualBoxInstaller.exe")
        try:
            print("Vérification de l'installation de VirtualBox...")
            try:
                resultat = subprocess.run([vboxmanage, "--version"], capture_output=True, text=True, check=True)
                print(f"VirtualBox est déjà installé. Version : {resultat.stdout.strip()}")
            except subprocess.CalledProcessError:
                print("VirtualBox n'est pas installé. Poursuite de l'installation...")
                subprocess.run(["powershell", "-Command", f"Invoke-WebRequest -Uri {virtualBoxUrl} -OutFile {destination}"], check=True)
                print("Téléchargement de VirtualBox terminé.")
                print("Lancement de l'installation...")
                subprocess.run([destination], check=True)
                print("Installation de VirtualBox terminée.")

            print("Création de la machine virtuelle...")
            name = input('Nom de la machine virtuelle : ')
            subprocess.run([vboxmanage, "createvm", "--name", name, "--ostype", "Linux_64", "--register"], check=True)
            subprocess.run([vboxmanage, "modifyvm", name, "--cpus", "2"], check=True)
            subprocess.run([vboxmanage, "storagectl", name, "--name", "IDE", "--add", "ide"], check=True)
            
            print("Téléchargement de l'ISO Linux...")
            chemin_actuel = os.getcwd()
            nom_fichier_iso = "debian-12.7.0-amd64-netinst.iso"
            chemin_iso = os.path.join(chemin_actuel, nom_fichier_iso)
            
            if os.path.exists(chemin_iso):
                print(f"L'ISO {nom_fichier_iso} est déjà téléchargé.")
                iso_url = chemin_iso
            else:
                print(f"L'ISO {nom_fichier_iso} n'est pas présent. Téléchargement en cours...")
                iso_url = wget("https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/debian-12.7.0-amd64-netinst.iso", chemin_actuel)

            print("Téléchargement de l'ISO terminé.")

            subprocess.run([vboxmanage, "storageattach", name, "--storagectl", "IDE", "--port", "0", "--device", "0", "--type", "dvddrive", "--medium", iso_url], check=True)
            resultat = subprocess.run([vboxmanage, "list", "vms"], capture_output=True, text=True)
            assert name in resultat.stdout, f"La machine virtuelle '{name}' n'a pas été créée avec succès."
            print("Machine virtuelle créée avec succès.")
        except subprocess.CalledProcessError as e:
            print(f"Erreur lors de l'installation de VirtualBox ou de la création de la machine virtuelle : {e}")

    elif platform.system() == "Linux":
        print("Installation de VirtualBox sur Linux...")
        subprocess.run(["sudo", "apt", "update", "&&", "sudo", "apt", "upgrade", "-y"], check=True)
        subprocess.run(["sudo", "apt", "install", "-y", "wget", "apt-transport-https", "software-properties-common"], check=True)
        subprocess.run(["wget", "-q", "https://www.virtualbox.org/download/oracle_vbox_2016.asc", "-O-", "|", "sudo", "apt-key", "add", "-"], check=True)
        subprocess.run(["echo", "deb [arch=amd64] https://download.virtualbox.org/virtualbox/debian $(lsb_release -cs) contrib", "|", 
                        "sudo", "tee", "/etc/apt/sources.list.d/virtualbox.list"], check=True)
        subprocess.run(["sudo", "apt", "update"], check=True)
        subprocess.run(["sudo", "apt", "install", "virtualbox-6.1", "-y"], check=True)
       
        print("Création de la machine virtuelle")
        name = input('Nom de la machine virtuelle : ')
        subprocess.run(["vboxmanage", "createvm", "--name", name, "--ostype", "Linux_64", "--register"], check=True)
        subprocess.run(["vboxmanage", "modifyvm", name, "--cpus", "2"], check=True)
        subprocess.run(["vboxmanage", "storagectl", name, "--name", "IDE", "--add", "ide"], check=True)
        
        print("Téléchargement de l'ISO Linux...")
        iso_url = "https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/debian-12.7.0-amd64-netinst.iso"
        if 'HOME' in os.environ:
            iso_destination = os.path.join(os.environ['HOME'], "debian.iso")
        else:
            iso_destination = os.path.join(os.path.expanduser('~'), "debian.iso")
        subprocess.run(["wget", "-O", iso_destination, iso_url], check=True)
        print("Téléchargement de l'ISO terminé.")

        subprocess.run(["vboxmanage", "storageattach", name, "--storagectl", "IDE", "--port", "0", "--device", "0", "--type", "dvddrive", "--medium", iso_destination], check=True)
        resultat = subprocess.run(["vboxmanage", "list", "vms"], capture_output=True, text=True)
        assert name in resultat.stdout, f"La machine virtuelle '{name}' n'a pas été créée avec succès."
        print("Machine virtuelle créée avec succès.")
    else:
        print("Système d'exploitation non pris en charge.")
        
def print_success(message):
    print(Fore.GREEN + Style.BRIGHT + message)

def print_error(message):
    print(Fore.RED + Style.BRIGHT + message)

def print_info(message):
    print(Fore.YELLOW + Style.BRIGHT + message)

def is_virtualbox_installed():
    try:
        if platform.system() == "Windows":
            vboxmanage = r"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"
            print_info(f"Vérification de l'installation de VirtualBox à l'emplacement: {vboxmanage}")
            subprocess.run([vboxmanage, '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        elif platform.system() == "Linux":
            print_info("Vérification de l'installation de VirtualBox avec 'vboxmanage'.")
            subprocess.run(['vboxmanage', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            print_error("OS non pris en compte")
            return False
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print_error(f"Erreur lors de la vérification de VirtualBox: {e}")
        return False

def install_links(os_type):
    return "https://www.virtualbox.org/wiki/Downloads"

def check_virtualbox(os_type):
    if is_virtualbox_installed():
        print_success("VirtualBox est installé.")
        return True
    else:
        print_error("VirtualBox n'est pas installé.")
        print_info(f"Vous pouvez le télécharger ici : {install_links(os_type)}")
        return False

init(autoreset=True)
