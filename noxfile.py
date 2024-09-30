import nox


@nox.session
def tests(session) -> None:
    """Runs the test suite."""
    session.install(".[test]")
    session.run("pytest")
