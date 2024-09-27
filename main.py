from docker import DockerManager

def main_menu():
    print("Menu principal:")
    print("1. Créer une VM (VirtualBox)")
    print("2. Créer un container (Docker)")
    
    while True:
        choice = input("Choisissez une option (1 ou 2) : ")
        if choice in ['1', '2']:
            break
        print("Option non valide. Veuillez choisir 1 ou 2.")

    if choice == "1":
        print("La création de VM VirtualBox n'est pas encore implémentée.")
    elif choice == "2":
        docker_manager = DockerManager()
        docker_manager.create_container()

if __name__ == "__main__":
    main_menu()
