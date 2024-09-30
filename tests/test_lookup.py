import pytest

from check_tests_structure.lookup import Lookup


@pytest.fixture
def mock_entries_list():
    return [
        {"dir": "/test_proj/dir1", "name": "file1", "original_name": "file1.py"},
        {"dir": "/test_proj/dir2", "name": "file2", "original_name": "file2.py"},
        {"dir": "/test_proj/dir3", "name": "file3", "original_name": "file3.py"},
    ]


@pytest.fixture
def mock_lookup(mock_entries_list):
    return Lookup(entries_list=mock_entries_list)


def test_exists(mock_lookup):
    assert mock_lookup.exists({"dir": "/test_proj/dir1", "name": "file1"})
    assert not mock_lookup.exists({"dir": "/test_proj/dir1", "name": "file2"})
    assert mock_lookup.exists({"dir": "/test_proj/dir2", "name": "file2"})
    assert not mock_lookup.exists({"dir": "/test_proj/dir2", "name": "file1"})


def test_fuzz_match(mock_lookup):
    matches = mock_lookup.fuzzy_match({"dir": "/test_proj/dir2", "name": "filee2"}, n_max=1)
    assert len(matches) == 1
    assert matches[0][0] == "/test_proj/dir2/file2"
    assert matches[0][1] > 97
    assert matches[0][2] == 1


def test_print_fuzzy_matches(mocker, mock_lookup, capsys):
    mocker.patch.object(Lookup, "fuzzy_match", return_value=[("/test_proj/dir2/file2", 97.7, 1)])
    mock_lookup.print_fuzzy_matches(
        {"dir": "/test_proj/dir2", "name": "filee2"}, "{dir}/{name} ({score:.1f}%)"
    )
    captured = capsys.readouterr()
    assert captured.out == "/test_proj/dir2/file2 (97.7%)\n"


def test_iter(mock_lookup):
    assert list(iter(mock_lookup)) == mock_lookup.entries_list


def test_len(mock_lookup):
    assert len(mock_lookup) == 3
