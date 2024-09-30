import nox


@nox.session
def tests(session) -> None:
    """Runs the test suite."""
    session.install(".[test]")
    session.run("pytest")


@nox.session
def try_hook(session) -> None:
    """Tests the pre-commit hook in this repo."""
    session.install("pre-commit")
    session.run("pre-commit", "try-repo", ".", "--verbose")


@nox.session
def licensecheck(session) -> None:
    """Runs the license check."""
    session.install("licensecheck")
    session.run("licensecheck")
