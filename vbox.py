import platform
import subprocess
from colorama import init, Fore, Style

# Initialiser colorama
init(autoreset=True)

def print_success(message):
    print(Fore.GREEN + Style.BRIGHT + message)

def print_error(message):
    print(Fore.RED + Style.BRIGHT + message)

def print_info(message):
    print(Fore.YELLOW + Style.BRIGHT + message)

def is_virtualbox_installed():
    """Vérifie si VirtualBox est installé en utilisant la commande 'vboxmanage' pour Linux et Windows."""
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
    """Renvoie le lien de téléchargement pour VirtualBox selon le système d'exploitation."""
    return "https://www.virtualbox.org/wiki/Downloads"

def check_virtualbox(os_type):
    if is_virtualbox_installed():
        print_success("VirtualBox est installé.")
        return True
    else:
        print_error("VirtualBox n'est pas installé.")
        print_info(f"Vous pouvez le télécharger ici : {install_links(os_type)}")
        return False
