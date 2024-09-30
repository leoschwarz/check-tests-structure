import cyclopts
import sys
from pathlib import Path
from check_tests_structure.compare import Compare
from check_tests_structure.config import Config, Paths

app = cyclopts.App()


@app.default
def check(sources_folder: Path, tests_folder: Path):
    compare = Compare(
        config=Config(), paths=Paths(sources=sources_folder, tests=tests_folder)
    )
    differences = compare.get_differences()
    compare.print_differences(differences)
    if differences["source"] or differences["test"]:
        sys.exit(1)


if __name__ == "__main__":
    app()
