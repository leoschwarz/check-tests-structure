import sys
from pathlib import Path

import cyclopts

from check_tests_structure.compare import Compare
from check_tests_structure.config import (
    Config,
    parse_pyproject_toml,
    find_pyproject_toml,
)

app = cyclopts.App()


def run_check(config: Config) -> None:
    compare = Compare(config=config)
    differences = compare.get_differences()
    compare.print_differences(differences)
    if (differences["source"] and not config.allow_missing_tests) or (
        differences["test"] and not config.allow_missing_sources
    ):
        sys.exit(1)


@app.default
def run(path: Path | None = None) -> None:
    # find the pyproject.toml
    pyproject_toml = find_pyproject_toml(path or Path.cwd())
    if not pyproject_toml:
        print("No pyproject.toml found.")
        sys.exit(1)

    # parse the pyproject.toml
    config = parse_pyproject_toml(pyproject_toml)

    # run the check
    run_check(config)


if __name__ == "__main__":
    app()
