import subprocess
from colorama import Fore, init

init(autoreset=True)

class DockerManager:
    def __init__(self):
        self.container_types = ["Ubuntu", "Debian", "RockyLinux", "Fedora", "Python", "MariaDB", "NixOS", "Kali"]

    def create_container(self):
        image = self._get_container_type()
        persistent_volume = self._ask_for_persistent_volume()

        cmd = ["docker", "run", "-d"]
        if persistent_volume:
            volume_name = self._create_volume(image)
            if volume_name:
                cmd.extend(["-v", f"{volume_name}:/data"])
            else:
                return

        cmd.append(image)
        self._run_docker_command(cmd)

    def _get_container_type(self):
        print("Quel type de conteneur souhaitez-vous créer ?")
        for i, type in enumerate(self.container_types, 1):
            print(f"{i}. {type}")
        
        while True:
            try:
                choice = int(input("Entrez le numéro correspondant : ")) - 1
                if 0 <= choice < len(self.container_types):
                    image = self.container_types[choice].lower()
                    return "nixos/nix" if image == "nixos" else "kalilinux/kali-rolling" if image == "kali" else image
                else:
                    print("Choix invalide. Veuillez réessayer.")
            except ValueError:
                print("Veuillez entrer un nombre valide.")

    def _ask_for_persistent_volume(self):
        return input("Voulez-vous rattacher un volume persistant ? (oui/non) : ").lower() == 'oui'

    def _create_volume(self, image):
        volume_name = f"{image.replace('/', '_')}_data"
        try:
            subprocess.run(["docker", "volume", "create", volume_name], check=True)
            print(Fore.GREEN + f"Volume {volume_name} créé avec succès.")
            return volume_name
        except subprocess.CalledProcessError as e:
            print(Fore.RED + f"Erreur lors de la création du volume : {e}")
            return None

    def _run_docker_command(self, cmd):
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            container_id = result.stdout.strip()
            print(Fore.GREEN + f"Conteneur créé avec succès. ID: {container_id}")
        except subprocess.CalledProcessError as e:
            print(Fore.RED + f"Erreur lors de la création du conteneur : {e}")
            print(Fore.RED + f"Sortie d'erreur : {e.stderr}")
