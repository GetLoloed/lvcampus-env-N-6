import platform
from docker import check_docker, create_docker_container
from vbox import check_virtualbox, vbox_install
from colorama import init, Fore, Style

init(autoreset=True)

def print_menu():
    print(Fore.CYAN + Style.BRIGHT + "Menu principal:")
    print("1. Créer un conteneur Docker")
    print("2. Créer une machine virtuelle")
    print("3. Quitter")

def main():
    os_type = platform.system()
    print(Fore.GREEN + Style.BRIGHT + f"Vous êtes sur {os_type}.")

    vbox_ok = check_virtualbox(os_type)
    docker_ok = check_docker(os_type)

    if vbox_ok and docker_ok:
        while True:
            print_menu()
            choice = input("Choisissez une option (1-3): ")
            
            if choice == "1":
                create_docker_container()
            elif choice == "2":
                vbox_install()
            elif choice == "3":
                print(Fore.YELLOW + "Au revoir!")
                break
            else:
                print(Fore.RED + "Option invalide. Veuillez réessayer.")
    else:
        print(Fore.RED + "Certaines vérifications ont échoué. Veuillez résoudre les problèmes avant de continuer.")
        if not vbox_ok:
            print(Fore.RED + "VirtualBox n'est pas correctement installé ou configuré.")
        if not docker_ok:
            print(Fore.RED + "Docker n'est pas correctement installé ou le service n'est pas en cours d'exécution.")

if __name__ == "__main__":
    main()

