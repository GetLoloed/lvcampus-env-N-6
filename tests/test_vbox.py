import pytest
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
