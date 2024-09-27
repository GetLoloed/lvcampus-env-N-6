import subprocess
import os
import platform
import requests
from urllib.parse import urlparse



def wget(url, output_directory='.'):
    try:
        # Obtenir le nom du fichier à partir de l'URL
        nom_fichier = os.path.basename(urlparse(url).path)
        if not nom_fichier:
            nom_fichier = 'index.html'

        # Créer le chemin complet du fichier de sortie
        chemin_fichier = os.path.join(output_directory, nom_fichier)

        # Télécharger le contenu
        print(f"Téléchargement de {url}")
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Lever une exception pour les erreurs HTTP

        # Écrire le contenu dans un fichier
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
    print("2. Quitter")
    
    choix = input("Veuillez entrer votre choix (1 ou 2) : ")
    
    if choix == "1":
        print("Création d'une nouvelle machine virtuelle...")
        if platform.system() == "Windows":
            vboxmanage = r"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"  
            print("Téléchargement de VirtualBox sur Windows...")
            virtualBoxUrl = "https://download.virtualbox.org/virtualbox/7.0.10/VirtualBox-7.0.10-158379-Win.exe"
            destination = os.path.join(os.environ['TEMP'], "VirtualBoxInstaller.exe")
            try:
                # Vérifier si VirtualBox est déjà installé
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
                # Utiliser VBoxManage via cmd
                subprocess.run([vboxmanage, "createvm", "--name", name, "--ostype", "Linux_64", "--register"], check=True)
                subprocess.run([vboxmanage, "modifyvm", name, "--cpus", "2"], check=True)
                subprocess.run([vboxmanage, "storagectl", name, "--name", "IDE", "--add", "ide"], check=True)
                # Télécharger l'ISO Linux
                print("Téléchargement de l'ISO Linux...")
                chemin_actuel = os.getcwd()
                # Vérifier si l'ISO est déjà téléchargé
                nom_fichier_iso = "debian-12.7.0-amd64-netinst.iso"
                chemin_iso = os.path.join(chemin_actuel, nom_fichier_iso)
                
                if os.path.exists(chemin_iso):
                    print(f"L'ISO {nom_fichier_iso} est déjà téléchargé.")
                    iso_url = chemin_iso
                else:
                    print(f"L'ISO {nom_fichier_iso} n'est pas présent. Téléchargement en cours...")
                    iso_url = wget("https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/debian-12.7.0-amd64-netinst.iso",chemin_actuel)

                print("Téléchargement de l'ISO terminé.")

                # Attacher l'ISO à la machine virtuelle
                subprocess.run([vboxmanage, "storageattach", name, "--storagectl", "IDE", "--port", "0", "--device", "0", "--type", "dvddrive", "--medium", iso_url], shell=True)
                # Vérifier si la VM a été créée avec succès
                resultat = subprocess.run([vboxmanage, "list", "vms"], capture_output=True, text=True, shell=True)
                assert name in resultat.stdout, f"La machine virtuelle '{name}' n'a pas été créée avec succès."
                print("Machine virtuelle créée avec succès.")
            except subprocess.CalledProcessError as e:
                print(f"Erreur lors de l'installation de VirtualBox ou de la création de la machine virtuelle : {e}")

        elif platform.system() == "Linux":
            print("Installation de VirtualBox sur Linux...")
            subprocess.run(["sudo", "apt", "install", "&&","apt","upgrade","-y"])
            subprocess.run(["sudo", "apt", "install", "-y", "wget", "apt-transport-https", "software-properties-common"])
            subprocess.run(["wget", "-q", "https://www.virtualbox.org/download/oracle_vbox_2016.asc", "-O-", "|", "sudo", "tee", "/usr/share/keyrings/oracle-virtualbox.asc"])
            subprocess.run(["echo", "deb [signed-by=/usr/share/keyrings/oracle-virtualbox.asc] https://download.virtualbox.org/virtualbox/debian $(lsb_release -cs) contrib", "|", 
                            "sudo", "tee", "/etc/apt/sources.list.d/virtualbox.list"])
            subprocess.run(["sudo", "apt", "update"])
            subprocess.run(["sudo", "apt", "install", "virtualbox", "-y"])
           
            print("creation de la machine virtuelle")
            name = input('Nom de la machine virtuelle : ')
            subprocess.run(["vboxmanage", "createvm", "--name", name, "--ostype", "Linux_64", "--register"])
            subprocess.run(["vboxmanage", "modifyvm", name, "--cpus", "2"])
            subprocess.run(["vboxmanage", "storagectl", name, "--name", "IDE", "--add", "ide"])
            # Télécharger l'ISO Linux
            print("Téléchargement de l'ISO Linux...")
            iso_url = "https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/debian-11.7.0-amd64-netinst.iso"
            iso_destination = os.path.join(os.environ['HOME'], "debian.iso")
            subprocess.run(["wget", "-O", iso_destination, iso_url], check=True)
            print("Téléchargement de l'ISO terminé.")

            # Attacher l'ISO à la machine virtuelle
            subprocess.run(["vboxmanage", "storageattach", name, "--storagectl", "IDE", "--port", "0", "--device", "0", "--type", "dvddrive", "--medium", iso_destination])
            # Vérifier si la VM a été créée avec succès
            resultat = subprocess.run(["vboxmanage", "list", "vms"], capture_output=True, text=True)
            assert name in resultat.stdout, f"La machine virtuelle '{name}' n'a pas été créée avec succès."
            print("Machine virtuelle créée avec succès.")
        else:
            print("Système d'exploitation non pris en charge.")
        
    elif choix == "2":
        print("Au revoir !")
    else:
        print("Choix invalide. Veuillez réessayer.")


