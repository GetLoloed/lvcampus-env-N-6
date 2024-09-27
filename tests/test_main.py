import pytest
from main import print_menu, main

def test_print_menu(capsys):
    """Test si le menu s'affiche correctement."""
    print_menu()
    captured = capsys.readouterr()
    assert "Menu principal:" in captured.out
    assert "1. Créer un conteneur Docker" in captured.out
    assert "2. Créer une machine virtuelle" in captured.out
    assert "3. Quitter" in captured.out

def test_main_menu_flow(mocker):
    """Test le flux du menu principal."""
    mock_check_virtualbox = mocker.patch('main.check_virtualbox', return_value=True)
    mock_check_docker = mocker.patch('main.check_docker', return_value=True)
    mock_create_docker_container = mocker.patch('main.create_docker_container')
    mock_vbox_install = mocker.patch('main.vbox_install')
    
    # Simuler les entrées utilisateur : créer un conteneur, créer une VM, puis quitter
    mocker.patch('builtins.input', side_effect=['1', '2', '3'])
    
    main()
    
    # Vérifier que les fonctions ont été appelées
    mock_check_virtualbox.assert_called_once()
    mock_check_docker.assert_called_once()
    mock_create_docker_container.assert_called_once()
    mock_vbox_install.assert_called_once()

def test_main_checks_fail(mocker, capsys):
    """Test le comportement lorsque les vérifications échouent."""
    mocker.patch('main.check_virtualbox', return_value=False)
    mocker.patch('main.check_docker', return_value=False)
    
    main()
    
    captured = capsys.readouterr()
    assert "Certaines vérifications ont échoué" in captured.out
    assert "VirtualBox n'est pas correctement installé ou configuré" in captured.out
    assert "Docker n'est pas correctement installé ou le service n'est pas en cours d'exécution" in captured.out
