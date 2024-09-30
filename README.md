# check-tests-structure
The goal of this project is to validate whether your tests folder structure matches your sources folder structure.
This can be useful for example, when setting up testing for a Python project where you want all modules to be tested.

## Installation
This project requires Python 3.11 or later.
Either install this package, e.g. with [pipx](https://pipx.pypa.io) or set up a pre-commit hook:

```toml
# pyproject.toml:
[tool.check-tests-structure]
sources_path = "src/my_package"
tests_path = "tests/unit"
```

```yaml
# pre-commit-config.yaml:
repos:
  - repo: https://github.com/leoschwarz/check-tests-structure
    rev: v0.1.0
    hooks:
      - id: check-tests-structure
```
