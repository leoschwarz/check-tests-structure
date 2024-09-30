from pathlib import Path

import pytest

from check_tests_structure.compare import Compare
from check_tests_structure.config import Config


@pytest.fixture
def mock_config():
    return Config(
        sources_path=Path("/dev/null/sources"),
        tests_path=Path("/dev/null/tests"),
    )


@pytest.fixture
def mock_compare(mock_config):
    return Compare(mock_config)


def test_get_name(mock_compare):
    assert "my_test" == mock_compare._get_test_name("test_my_test.py")
