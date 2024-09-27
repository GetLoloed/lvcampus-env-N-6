import pytest
from docker import DockerManager
import subprocess

@pytest.fixture
def docker_manager():
    return DockerManager()

def test_get_container_type(docker_manager, mocker):
    mocker.patch('builtins.input', return_value='1')
    assert docker_manager._get_container_type() == 'ubuntu'

def test_ask_for_persistent_volume(docker_manager, mocker):
    mocker.patch('builtins.input', return_value='oui')
    assert docker_manager._ask_for_persistent_volume() == True

def test_create_volume_success(docker_manager, mocker):
    mock_run = mocker.patch('subprocess.run')
    assert docker_manager._create_volume('ubuntu') == 'ubuntu_data'
    mock_run.assert_called_once_with(['docker', 'volume', 'create', 'ubuntu_data'], check=True)

def test_create_volume_failure(docker_manager, mocker):
    mocker.patch('subprocess.run', side_effect=subprocess.CalledProcessError(1, 'cmd'))
    assert docker_manager._create_volume('ubuntu') is None

def test_run_docker_command_success(docker_manager, mocker, capsys):
    mock_run = mocker.patch('subprocess.run')
    mock_run.return_value.stdout = 'container_id_123'
    docker_manager._run_docker_command(['docker', 'run', '-d', 'ubuntu'])
    captured = capsys.readouterr()
    assert "Conteneur créé avec succès. ID: container_id_123" in captured.out

def test_run_docker_command_failure(docker_manager, mocker, capsys):
    mocker.patch('subprocess.run', side_effect=subprocess.CalledProcessError(1, 'cmd', stderr='Error message'))
    docker_manager._run_docker_command(['docker', 'run', '-d', 'ubuntu'])
    captured = capsys.readouterr()
    assert "Erreur lors de la création du conteneur :" in captured.out
    assert "Sortie d'erreur : Error message" in captured.out

def test_create_container(docker_manager, mocker):
    mocker.patch.object(docker_manager, '_get_container_type', return_value='ubuntu')
    mocker.patch.object(docker_manager, '_ask_for_persistent_volume', return_value=True)
    mocker.patch.object(docker_manager, '_create_volume', return_value='ubuntu_data')
    mock_run_docker = mocker.patch.object(docker_manager, '_run_docker_command')
    
    docker_manager.create_container()
    
    mock_run_docker.assert_called_once_with(['docker', 'run', '-d', '-v', 'ubuntu_data:/data', 'ubuntu'])