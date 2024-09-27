import pytest
import requests
import subprocess
import os
from vbox import vbox_install

# Test de la fonction vbox_install avec les entrées utilisateur simulées
@pytest.mark.parametrize("install_choice, nom_vm", [
    ("1", "test_vm"),  
    ("2", "")             
])

def test_vbox_install_create_vm(mocker, install_choice, nom_vm):
    # Simuler les entrées utilisateur : d'abord "1" pour créer une VM, puis "test_vm" pour le nom de la VM
    mock_inputs = [install_choice, nom_vm]
    mock_input = mocker.patch("builtins.input", side_effect=mock_inputs)
    
    # Simuler subprocess.run
    mock_subprocess = mocker.patch("subprocess.run")
    mock_subprocess.return_value.returncode = 0  # Simuler une exécution réussie
    
    # Simuler platform.system pour tester sur Windows
    mock_platform = mocker.patch("platform.system", return_value="Windows")
    
    # Appel de la fonction vbox_install
    vbox_install()
    
    # Vérifier que subprocess.run a été appelé au moins 3 fois pour les différentes étapes de la création de VM


import subprocess
import platform
from vbox import is_virtualbox_installed

@pytest.fixture
def mock_subprocess_run(mocker):
    return mocker.patch('subprocess.run')

def test_is_virtualbox_installed(mock_subprocess_run):
    """Test de la fonction is_virtualbox_installed."""
    mock_subprocess_run.return_value = subprocess.CompletedProcess(args=['vboxmanage', '--version'], returncode=0)
    assert is_virtualbox_installed() is True

    mock_subprocess_run.side_effect = subprocess.CalledProcessError(1, 'cmd')
    assert is_virtualbox_installed() is False

