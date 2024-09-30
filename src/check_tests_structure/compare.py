from __future__ import annotations
from check_tests_structure.config import Config, Paths


class Compare:
    def __init__(self, config: Config, paths: Paths):
        self._config = config
        self._paths = paths

    def get_differences(self):
        source_files = self.list_sources()
        test_files = self.list_tests()

        # will contain the files only present in either the source or test folder
        differences = {"source": [], "test": []}

        # Note: inefficient initial implementation
        for source_file in source_files:
            if not self._file_exists(source_file, test_files):
                differences["source"].append(source_file)
        for test_file in test_files:
            if not self._file_exists(test_file, source_files):
                differences["test"].append(test_file)

        return differences

    def print_differences(self):
        differences = self.get_differences()
        if not differences["source"] and not differences["test"]:
            print("No differences found.")
            return
        if differences["source"]:
            print("Source files not in test folder:")
            for source in differences["source"]:
                print(f"  {source['dir']}/{source['original_name']}")
        if differences["test"]:
            print("Test files not in source folder:")
            for test in differences["test"]:
                print(f"  {test['dir']}/{test['original_name']}")

    def list_sources(self) -> list[dict[str, str]]:
        """Lists all source files in the sources folder, relative to the sources folder."""
        paths = {
            path.relative_to(self._paths.sources)
            for glob_pattern in self._config.inputs_glob
            for path in self._paths.sources.rglob(glob_pattern)
            if path.name not in self._config.excluded_files
        }
        return [
            {"dir": str(path.parent), "original_name": path.name, "name": path.stem}
            for path in sorted(paths)
        ]

    def list_tests(self) -> list[dict[str, str]]:
        """Lists all test files in the tests folder, relative to the tests folder."""
        paths = {
            path.relative_to(self._paths.tests)
            for glob_pattern in self._config.tests_glob
            for path in self._paths.tests.rglob(glob_pattern)
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
        return [entry for entry in entries if entry["name"] is not None]

    def _get_test_name(self, filename: str) -> str | None:
        """Extracts the test name from the test filename."""
        matching = self._config.tests_pattern.match(filename)
        return matching.group(1) if matching else None

    def _file_exists(
        self, entry: dict[str, str], entries_list: list[dict[str, str]]
    ) -> bool:
        for entry_ in entries_list:
            if entry["dir"] == entry_["dir"] and entry["name"] == entry_["name"]:
                return True
        return False
