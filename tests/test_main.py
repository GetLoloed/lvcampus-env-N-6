import pytest
from main import print_menu, main

def test_print_menu(capsys):
    """Test si le menu s'affiche correctement."""
    print_menu()
    captured = capsys.readouterr()
    assert "Menu principal:" in captured.out
    assert "1. Créer un conteneur Docker" in captured.out
    assert "2. Quitter" in captured.out

def test_main_menu_flow(mocker):
    """Test le flux du menu principal."""
    # Simuler que VirtualBox et Docker sont correctement installés
    mocker.patch('main.check_virtualbox', return_value=True)
    mocker.patch('main.check_docker', return_value=True)
    
    # Simuler les entrées utilisateur : d'abord choisir de créer un conteneur, puis quitter
    mocker.patch('builtins.input', side_effect=['1', '2'])
    
    mock_create_docker = mocker.patch('main.create_docker_container')
    
    main()
    
    # Vérifier que create_docker_container a été appelé une fois
    mock_create_docker.assert_called_once()

def test_main_checks_fail(mocker, capsys):
    """Test le comportement lorsque les vérifications échouent."""
    mocker.patch('main.check_virtualbox', return_value=False)
    mocker.patch('main.check_docker', return_value=False)
    
    main()
    
    captured = capsys.readouterr()
    assert "Certaines vérifications ont échoué" in captured.out
    assert "VirtualBox n'est pas correctement installé ou configuré" in captured.out
    assert "Docker n'est pas correctement installé ou le service n'est pas en cours d'exécution" in captured.out
