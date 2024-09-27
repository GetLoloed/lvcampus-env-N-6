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

def obtenir_OS_info():
    os_info = platform.uname()
    type_systeme = os_info.system
    system_info = {
        'System Type': type_systeme
    }
    return system_info

def is_docker_installed():
    """Vérifie si Docker est installé."""
    try:
        subprocess.run(["docker", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print_success("Docker Desktop est installé.")
        return True
    except subprocess.CalledProcessError:
        print_error("Docker n'est pas installé.")
        return False

def is_docker_service_running():
    """Vérifie si Docker est actif en exécutant une commande simple."""
    try:
        subprocess.run(['docker', 'info'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
        print_success("Docker est actif et répond correctement.")
        return True
    except subprocess.CalledProcessError:
        print_error("Docker est installé mais ne répond pas correctement.")
        return False
    except subprocess.TimeoutExpired:
        print_error("La commande Docker a expiré. Docker pourrait être bloqué ou ne pas répondre.")
        return False
    except FileNotFoundError:
        print_error("La commande Docker n'a pas été trouvée. Docker pourrait ne pas être installé correctement.")
        return False
    except Exception as e:
        print_error(f"Une erreur inattendue s'est produite lors de la vérification de Docker : {e}")
        return False

def install_links(os_type):
    """Renvoie le lien de téléchargement pour Docker selon le système d'exploitation."""
    if os_type == "Windows" or os_type == "Darwin":
        return "https://www.docker.com/products/docker-desktop"
    elif os_type == "Linux":
        return "https://docs.docker.com/engine/install/"
    else:
        return None

def check_docker(os_type):
    if not is_docker_installed():
        print_error("Docker n'est pas installé.")
        print_info(f"Vous pouvez le télécharger ici : {install_links(os_type)}")
    else:
        print_success("Docker est installé.")
        docker_status = is_docker_service_running()
        if docker_status:
            print_success("Le service Docker est actif et fonctionne correctement.")
        else:
            print_error("Docker est installé, mais il y a un problème avec le service.")
            print_info("Veuillez vérifier que le service Docker est démarré et qu'il fonctionne correctement.")
            print_info("Vous pouvez essayer de redémarrer Docker ou consulter les logs pour plus d'informations.")