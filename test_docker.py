import pytest
import subprocess
import platform
from docker import is_virtualbox_installed, is_docker_installed, is_docker_service_running

# Mocking subprocess.run for testing purposes
@pytest.fixture(autouse=True)
def mock_subprocess_run(monkeypatch):
    def mock_run(*args, **kwargs):
        if args[0] == ['vboxmanage', '--version']:
            return subprocess.CompletedProcess(args, 0)  # Simulate success for vboxmanage
        elif args[0] == r"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe":
            return subprocess.CompletedProcess(args, 0)  # Simulate success for Windows
        elif args[0] == ["docker", "--version"]:
            return subprocess.CompletedProcess(args, 0)  # Simulate success for Docker
        elif args[0] == ['systemctl', 'is-active', '--quiet', 'docker']:
            return subprocess.CompletedProcess(args, 0)  # Simulate Docker service active on Linux
        elif args[0] == ['sc', 'query', 'docker']:
            return subprocess.CompletedProcess(args, 0)  # Simulate Docker service active on Windows
        raise subprocess.CalledProcessError(returncode=1, cmd=args)  # Simulate failure for other commands

    monkeypatch.setattr(subprocess, 'run', mock_run)

def test_is_virtualbox_installed():
    """Test de la fonction is_virtualbox_installed."""
    if platform.system() == "Windows":
        assert is_virtualbox_installed() is True
    elif platform.system() == "Linux":
        assert is_virtualbox_installed() is True
    else:
        assert is_virtualbox_installed() is False  # Non pris en compte

def test_is_docker_installed():
    """Test de la fonction is_docker_installed."""
    assert is_docker_installed() is True

def test_is_docker_service_running():
    """Test de la fonction is_docker_service_running."""
    if platform.system() == "Linux":
        assert is_docker_service_running() is True
    elif platform.system() == "Windows":
        assert is_docker_service_running() is True
    else:
        assert is_docker_service_running() is False  # Non pris en compte
