import platform
import subprocess
import os
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
        print_error("Docker est installé mais n'est pas lancé. Veuillez lancer Docker Desktop et recommencer")
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
        return False
    else:
        print_success("Docker est installé.")
        docker_status = is_docker_service_running()
        if docker_status:
            print_success("Le service Docker est actif et fonctionne correctement.")
            return True
        else:
            print_error("Docker est installé, mais il y a un problème avec le service.")
            print_info("Veuillez vérifier que le service Docker est démarré et qu'il fonctionne correctement.")
            print_info("Vous pouvez essayer de redémarrer Docker ou consulter les logs pour plus d'informations.")
            return False

def create_docker_container():
    print_info("Création d'un conteneur Docker")
    
    container_types = ["Ubuntu", "Debian", "RockyLinux", "Fedora", "Python", "MariaDB", "NixOS", "Kali"]
    print("Types de conteneurs disponibles:")
    for i, container_type in enumerate(container_types, 1):
        print(f"{i}. {container_type}")
    
    while True:
        choice = input(f"Choisissez le type de conteneur (1-{len(container_types)}): ")
        if choice.isdigit() and 1 <= int(choice) <= len(container_types):
            container_type = container_types[int(choice) - 1]
            break
        else:
            print_error("Choix invalide. Veuillez réessayer.")
    
    volume = input("Voulez-vous attacher un volume persistant? (o/n): ").lower() == 'o'
    
    try:
        # Déterminer l'image Docker à utiliser
        if container_type == "Ubuntu":
            image = "ubuntu:latest"
        elif container_type == "Debian":
            image = "debian:latest"
        elif container_type == "RockyLinux":
            image = "rockylinux/rockylinux:latest"
        elif container_type == "Fedora":
            image = "fedora:latest"
        elif container_type == "Python":
            image = "python:latest"
        elif container_type == "MariaDB":
            image = "mariadb:latest"
        elif container_type == "NixOS":
            image = "nixos/nix:latest"
        elif container_type == "Kali":
            image = "kalilinux/kali-rolling:latest"
        else:
            image = f"{container_type.lower()}:latest"
        
        # Télécharger l'image Docker
        print_info(f"Téléchargement de l'image Docker {image}...")
        subprocess.run(["docker", "pull", image], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print_success(f"Image {image} téléchargée avec succès.")
        
        cmd = ["docker", "run", "-d"]
        if volume:
            volume_name = f"{container_type.lower()}_volume"
            create_volume_cmd = ["docker", "volume", "create", volume_name]
            subprocess.run(create_volume_cmd, check=True)
            print_success(f"Volume Docker créé : {volume_name}")
            cmd.extend(["-v", f"{volume_name}:/data"])
            print_info(f"Volume {volume_name} monté sur /data dans le conteneur")
        
        container_name = f"{container_type.lower()}-container-{os.urandom(4).hex()}"
        cmd.extend(["--name", container_name])
        
        cmd.append(image)
        
        if platform.system() == "Linux":
            # Vérifier si l'utilisateur est dans le groupe docker
            try:
                subprocess.run(["docker", "info"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except subprocess.CalledProcessError:
                print_error("Vous n'avez pas les permissions pour exécuter Docker.")
                print_info("Essayez d'ajouter votre utilisateur au groupe docker avec la commande:")
                print_info("sudo usermod -aG docker $USER")
                print_info("Puis déconnectez-vous et reconnectez-vous pour que les changements prennent effet.")
                return

        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        container_id = result.stdout.strip()
        print_success(f"Conteneur {container_type} créé avec succès. Nom: {container_name}, ID: {container_id}")
        
        if volume:
            print_info(f"Pour vérifier le volume, utilisez la commande:")
            print_info(f"docker inspect -f '{{{{ .Mounts }}}}' {container_name}")
            
            print_info(f"Vérification du volume pour le conteneur {container_name}...")
            inspect_cmd = ["docker", "inspect", "-f", "{{ .Mounts }}", container_name]
            inspect_result = subprocess.run(inspect_cmd, capture_output=True, text=True)
            print_info(f"Résultat de l'inspection : {inspect_result.stdout}")
            
            print_info(f"Vérification du montage du volume dans le conteneur {container_name}...")
            exec_cmd = ["docker", "exec", container_name, "ls", "-l", "/data"]
            exec_result = subprocess.run(exec_cmd, capture_output=True, text=True)
            print_info(f"Contenu du répertoire /data dans le conteneur : {exec_result.stdout}")
    except subprocess.CalledProcessError as e:
        print_error(f"Erreur lors de la création du conteneur {container_type}: {e}")
    except Exception as e:
        print_error(f"Une erreur inattendue s'est produite: {e}")