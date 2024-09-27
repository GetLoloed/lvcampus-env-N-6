import pytest
import requests
import subprocess
import os
from vbox import vbox_install, create_virtual_machine, is_virtualbox_installed

@pytest.mark.parametrize("choix_installation, nom_vm", [
    ("1", "test_vm"),  
    ("2", "")             
])
def test_vbox_install_creer_vm(mocker, choix_installation, nom_vm):
    # Simuler les entrées utilisateur
    entrees_simulees = [choix_installation, nom_vm]
    mocker.patch("builtins.input", side_effect=entrees_simulees)
    
    # Simuler subprocess.run
    mock_subprocess = mocker.patch("subprocess.run")
    mock_subprocess.return_value.returncode = 0
    mock_subprocess.return_value.stdout = f'"{nom_vm}"'
    

    # Simuler platform.system pour tester sur Windows et Linux
    systemes = ["Windows", "Linux"]
    for systeme in systemes:
        mocker.patch("platform.system", return_value=systeme)
        
        # Simuler os.path.exists pour éviter le téléchargement de l'ISO
        mocker.patch("os.path.exists", return_value=True)
        
        # Simuler wget pour éviter le téléchargement réel
        mocker.patch("vbox.wget", return_value="chemin/simule/de/iso")
        
        # Appeler la fonction vbox_install
        vbox_install()
        
        if choix_installation == "1":
            # Vérifier que subprocess.run a été appelé pour créer la VM
            assert any("createvm" in str(appel) for appel in mock_subprocess.call_args_list)
            # Vérifier que le nom de la VM est utilisé dans les appels
            assert any(nom_vm in str(appel) for appel in mock_subprocess.call_args_list)
        else:
            # Vérifier qu'aucune VM n'a été créée si l'option 2 est choisie
            assert not any("createvm" in str(appel) for appel in mock_subprocess.call_args_list)
        
        # Réinitialiser les mocks pour le prochain système
        mock_subprocess.reset_mock()

@pytest.fixture
def mock_subprocess_run(mocker):
    return mocker.patch('subprocess.run')

def test_is_virtualbox_installed(mock_subprocess_run):
    """Test de la fonction is_virtualbox_installed."""
    mock_subprocess_run.return_value = subprocess.CompletedProcess(args=['vboxmanage', '--version'], returncode=0)
    assert is_virtualbox_installed() is True

    mock_subprocess_run.side_effect = subprocess.CalledProcessError(1, 'cmd')
    assert is_virtualbox_installed() is False

