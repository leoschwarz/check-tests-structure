import sys
from pathlib import Path

import cyclopts

from check_tests_structure.compare import Compare
from check_tests_structure.config import Config

app = cyclopts.App()


@app.default
def check(sources_folder: Path, tests_folder: Path):
    config = Config(sources_path=sources_folder, tests_path=tests_folder)
    compare = Compare(config=config)
    differences = compare.get_differences()
    compare.print_differences(differences)
    if (differences["source"] and not config.allow_missing_sources) or (
        differences["test"] and not config.allow_missing_tests
    ):
        sys.exit(1)


if __name__ == "__main__":
    app()
