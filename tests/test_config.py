from pathlib import Path

from check_tests_structure.config import find_pyproject_toml, parse_pyproject_toml


def test_find_pyproject_toml_initial_when_project_root(fs):
    fs.create_file("/my_project/pyproject.toml")
    assert find_pyproject_toml(Path("/my_project")) == Path("/my_project/pyproject.toml")


def test_find_pyproject_toml_initial_when_passed_already(fs):
    fs.create_file("/my_project/pyproject.toml")
    assert find_pyproject_toml(Path("/my_project/pyproject.toml")) == Path("/my_project/pyproject.toml")


def test_find_pyproject_toml_when_sub_directory(fs):
    fs.create_file("/my_project/pyproject.toml")
    assert find_pyproject_toml(Path("/my_project/subdir")) == Path("/my_project/pyproject.toml")


def test_find_pyproject_toml_when_sub_sub_directory(fs):
    fs.create_file("/my_project/pyproject.toml")
    assert find_pyproject_toml(Path("/my_project/subdir/subsubdir")) == Path("/my_project/pyproject.toml")


def test_find_pyproject_toml_when_not_found(fs):
    assert find_pyproject_toml(Path("/my_project")) is None


def test_parse_pyproject_toml_when_minimal(mocker):
    mock_path = mocker.Mock()
    mock_path.read_text.return_value = """
    [tool.check-tests-structure]
    sources_path = "src"
    tests_path = "tests"
    """
    config = parse_pyproject_toml(path=mock_path)
    assert config.sources_path == Path("src")
    assert config.tests_path == Path("tests")
