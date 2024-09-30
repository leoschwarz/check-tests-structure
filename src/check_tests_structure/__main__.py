import cyclopts
from pathlib import Path
from check_tests_structure.compare import Compare
from check_tests_structure.config import Config, Paths

app = cyclopts.App()


@app.default
def check(sources_folder: Path, tests_folder: Path):
    compare = Compare(
        config=Config(), paths=Paths(sources=sources_folder, tests=tests_folder)
    )
    compare.print_differences()


if __name__ == "__main__":
    app()
