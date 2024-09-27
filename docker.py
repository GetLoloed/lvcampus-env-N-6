import platform
import os
import subprocess

def obtenir_OS_info():
    os_info = platform.uname()
    type_systeme = os_info.system
    system_info = {
        'System Type': type_systeme
    }
    return system_info

def is_virtualbox_installed():
    """Vérifie si VirtualBox est installé en utilisant la commande 'vboxmanage' pour Linux et Windows."""
    try:
        if platform.system() == "Windows":
            # Commande pour vérifier VirtualBox sur Windows
            vboxmanage = r"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"
            print(f"Vérification de l'installation de VirtualBox à l'emplacement: {vboxmanage}")
            subprocess.run([vboxmanage, '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        elif platform.system() == "Linux":
            # Commande pour vérifier VirtualBox sur Linux
            print("Vérification de l'installation de VirtualBox avec 'vboxmanage'.")
            subprocess.run(['vboxmanage', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
        else:
            print("OS non pris en compte")
            return False
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Erreur lors de la vérification de VirtualBox: {e}")
        return False
    
def is_docker_installed():
    """Vérifie si Docker est installé."""
    try:
        subprocess.run(["docker", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Docker Desktop est installé.")
        return True
    except subprocess.CalledProcessError:
        return False
    

def is_docker_service_running():
    """Vérifie si le service Docker est actif."""
    try:
        if platform.system() == "Linux":
            print("Vérification de l'état du service Docker sur Linux.")
            result = subprocess.run(['systemctl', 'is-active', '--quiet', 'docker'])
            return result.returncode == 0
        elif platform.system() == "Windows":
            print("Vérification de l'état du service Docker sur Windows.")
            result = subprocess.run(['sc', 'query', 'docker'], capture_output=True, text=True)
            print(f"Sortie de la commande: {result.stdout}")
            return "RUNNING" in result.stdout
        else:
            print("Vérification du service Docker n'est pas supportée pour cet OS.")
            return False
    except Exception as e:
        print(f"Erreur lors de la vérification du service Docker : {e}")
        return False

def install_links(os_type):
    """Renvoie les liens de téléchargement pour VirtualBox et Docker selon le système d'exploitation."""
    if os_type == "Windows":
        return {
            "VirtualBox": "https://www.virtualbox.org/wiki/Downloads",
            "Docker": "https://www.docker.com/products/docker-desktop"
        }
    elif os_type == "Linux":
        return {
            "VirtualBox": "https://www.virtualbox.org/wiki/Downloads",
            "Docker": "https://docs.docker.com/engine/install/"
        }
    elif os_type == "Darwin":
        return {
            "VirtualBox": "https://www.virtualbox.org/wiki/Downloads",
            "Docker": "https://www.docker.com/products/docker-desktop"
        }
    else:
        return None

def main():
    os_type = platform.system()
    print(f"Vous êtes sur {os_type}.")

    # Vérification de VirtualBox
    if not is_virtualbox_installed():
        print("VirtualBox n'est pas installé.")
        print(f"Vous pouvez le télécharger ici : {install_links(os_type)['VirtualBox']}")
    else:
        print("VirtualBox est installé.")

    # Vérification de Docker
    if not is_docker_installed():
        print("Docker n'est pas installé.")
        print(f"Vous pouvez le télécharger ici : {install_links(os_type)['Docker']}")
    else:
        # Vérification si le service Docker est en cours d'exécution
        if not is_docker_service_running():
            print("Le service Docker n'est pas actif. Tentative de démarrage...")
            try:
                if os_type == "Linux":
                    subprocess.run(['sudo', 'systemctl', 'start', 'docker'], check=True)
                    print("Le service Docker a été démarré.")
                elif os_type == "Windows":
                    subprocess.run(['sc', 'start', 'docker'], check=True)
                    print("Le service Docker a été démarré.")
            except subprocess.CalledProcessError:
                print("Erreur lors du démarrage du service Docker.")
        else:
            print("Le service Docker est actif.")

if __name__ == "__main__":
    main()