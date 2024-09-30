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
    if (differences["source"] and not config.allow_missing_sources) or (
        differences["test"] and not config.allow_missing_tests
    ):
        sys.exit(1)


@app.command
def check(sources_folder: Path, tests_folder: Path):
    config = Config(sources_path=sources_folder, tests_path=tests_folder)
    run_check(config)


@app.command
def hook():
    # find the pyproject.toml
    pyproject_toml = find_pyproject_toml(Path.cwd())
    if not pyproject_toml:
        print("No pyproject.toml found.")
        sys.exit(1)

    # parse the pyproject.toml
    config = parse_pyproject_toml(pyproject_toml)

    # run the check
    run_check(config)


if __name__ == "__main__":
    app()
