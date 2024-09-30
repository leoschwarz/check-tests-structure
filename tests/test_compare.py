import pytest
from pathlib import Path
from check_tests_structure.config import Config, Paths
from check_tests_structure.compare import Compare


@pytest.fixture
def mock_config():
    return Config()


@pytest.fixture
def mock_paths():
    return Paths(sources=Path("/dev/null/sources"), tests=Path("/dev/null/tests"))


@pytest.fixture
def mock_compare(mock_config, mock_paths):
    return Compare(mock_config, mock_paths)


def test_get_name(mock_compare):
    assert "my_test" == mock_compare._get_test_name("test_my_test.py")
