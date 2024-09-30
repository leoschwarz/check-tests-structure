from __future__ import annotations

from functools import cached_property

from check_tests_structure.config import Config
from check_tests_structure.lookup import Lookup


class Compare:
    def __init__(self, config: Config):
        self._config = config

    def get_differences(self) -> dict[str, list[dict[str, str]]]:
        """Returns the differences between the source and test files.
        This will be a dictionary with two keys: 'source' and 'test', each containing a list of entries of the
        files that are only present in that particular folder.
        """
        differences = {"source": [], "test": []}
        for source_file in self.source_files:
            if not self.test_files.exists(source_file):
                differences["source"].append(source_file)
        for test_file in self.test_files:
            if not self.source_files.exists(test_file):
                differences["test"].append(test_file)
        return differences

    def print_differences(self, differences: dict[str, list[dict[str, str]]]) -> None:
        """Prints the differences between the source and test files."""
        if not differences["source"] and not differences["test"]:
            print("No differences found.")
            return
        if differences["source"]:
            print("Source files not in test folder:")
            for source in differences["source"]:
                print(f"  {source['dir']}/{source['original_name']}")
                self.test_files.print_fuzzy_matches(
                    source, "    - {dir}/{original_name} ({score:.1f}% match)"
                )
        if differences["test"]:
            print("Test files not in source folder:")
            for test in differences["test"]:
                print(f"  {test['dir']}/{test['original_name']}")
                self.source_files.print_fuzzy_matches(
                    test, "    - {dir}/{original_name} ({score:.1f}% match)"
                )

    @cached_property
    def source_files(self) -> Lookup:
        """Lists all source files in the sources folder, relative to the sources folder."""
        paths = {
            path.relative_to(self._config.sources_path)
            for glob_pattern in self._config.inputs_glob
            for path in self._config.sources_path.rglob(glob_pattern)
            if path.name not in self._config.excluded_files
        }
        return Lookup(
            [
                {"dir": str(path.parent), "original_name": path.name, "name": path.stem}
                for path in sorted(paths)
            ]
        )

    @cached_property
    def test_files(self) -> Lookup:
        """Lists all test files in the tests folder, relative to the tests folder."""
        paths = {
            path.relative_to(self._config.tests_path)
            for glob_pattern in self._config.tests_glob
            for path in self._config.tests_path.rglob(glob_pattern)
            if path.name not in self._config.excluded_files
        }
        entries = [
            {
                "dir": str(path.parent),
                "original_name": path.name,
                "name": self._get_test_name(path.name),
            }
            for path in sorted(paths)
        ]
        return Lookup([entry for entry in entries if entry["name"] is not None])

    def _get_test_name(self, filename: str) -> str | None:
        """Extracts the test name from the test filename."""
        matching = self._config.tests_pattern.match(filename)
        return matching.group(1) if matching else None
