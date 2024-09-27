import platform
from docker import check_docker
from vbox import check_virtualbox

def main():
    os_type = platform.system()
    print(f"Vous êtes sur {os_type}.")

    # Vérification de VirtualBox
    check_virtualbox(os_type)

    # Vérification de Docker
    check_docker(os_type)

if __name__ == "__main__":
    main()
