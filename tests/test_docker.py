import pytest
import subprocess
import platform
from docker import is_docker_installed, is_docker_service_running, check_docker, create_docker_container, install_links

@pytest.fixture
def mock_subprocess_run(mocker):
    return mocker.patch('subprocess.run')

def test_is_docker_installed(mock_subprocess_run):
    """Test de la fonction is_docker_installed."""
    mock_subprocess_run.return_value = subprocess.CompletedProcess(args=['docker', '--version'], returncode=0)
    assert is_docker_installed() is True

    mock_subprocess_run.side_effect = subprocess.CalledProcessError(1, 'cmd')
    assert is_docker_installed() is False

def test_is_docker_service_running(mock_subprocess_run):
    """Test de la fonction is_docker_service_running."""
    mock_subprocess_run.return_value = subprocess.CompletedProcess(args=['docker', 'info'], returncode=0)
    assert is_docker_service_running() is True

    mock_subprocess_run.side_effect = subprocess.CalledProcessError(1, 'cmd')
    assert is_docker_service_running() is False

def test_check_docker(mock_subprocess_run):
    """Test de la fonction check_docker."""
    mock_subprocess_run.return_value = subprocess.CompletedProcess(args=['docker', '--version'], returncode=0)
    assert check_docker('Linux') == True

    mock_subprocess_run.side_effect = [
        subprocess.CompletedProcess(args=['docker', '--version'], returncode=0),
        subprocess.CalledProcessError(1, 'docker info')
    ]
    assert check_docker('Linux') == False

def test_create_docker_container(mocker, mock_subprocess_run):
    """Test de la fonction create_docker_container."""
    mocker.patch('builtins.input', side_effect=['1', 'o'])
    mock_subprocess_run.return_value = subprocess.CompletedProcess(args=['docker', 'run'], returncode=0, stdout='container_id')

    mocker.patch('docker.print_success')
    mocker.patch('docker.print_info')

    create_docker_container()

    print("Nombre d'appels à subprocess.run:", mock_subprocess_run.call_count)
    print("Appels effectués:")
    for call in mock_subprocess_run.call_args_list:
        print(call)

    assert mock_subprocess_run.call_count >= 3  # Au moins 3 appels : pull, volume create, run

    # Vérifier que les commandes Docker appropriées ont été appelées
    calls = mock_subprocess_run.call_args_list
    assert any(['docker', 'pull', 'ubuntu:latest'] == call[0][0] for call in calls), "La commande 'docker pull ubuntu:latest' n'a pas été appelée"
    assert any(['docker', 'volume', 'create'] == call[0][0][:3] for call in calls), "La commande 'docker volume create' n'a pas été appelée"
    assert any(['docker', 'run', '-d'] == call[0][0][:3] and '-v' in call[0][0] for call in calls), "La commande 'docker run' avec l'option '-v' n'a pas été appelée"

@pytest.mark.parametrize("os_type,expected", [
    ("Windows", "https://www.docker.com/products/docker-desktop"),
    ("Darwin", "https://www.docker.com/products/docker-desktop"),
    ("Linux", "https://docs.docker.com/engine/install/"),
    ("Other", None)
])
def test_install_links(os_type, expected):
    """Test de la fonction install_links."""
    assert install_links(os_type) == expected
