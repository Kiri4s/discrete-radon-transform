"""Nox sessions."""

import nox
import tempfile
from nox.sessions import Session
from typing import Any


def install_with_constraints(session: Session, *args: str, **kwargs: Any) -> None:
    """Install packages constrained by Poetry's lock file."""


def black(session: Session) -> None:
    """Run black code formatter."""


def lint(session: Session) -> None:
    """Lint using flake8."""


def safety(session: Session) -> None:
    """Scan dependencies for insecure packages."""


def mypy(session: Session) -> None:
    """Type-check using mypy."""


def pytype(session: Session) -> None:
    """Type-check using pytype."""


def tests(session: Session) -> None:
    """Run the test suite."""


def typeguard(session: Session) -> None:
    """Runtime type checking using Typeguard."""


locations = "discrete_radon_transform", "tests", "noxfile.py", "docs/conf.py"
nox.options.sessions = "safety", "mypy", "tests", "pytype"


def install_with_constraints(session, *args, **kwargs):
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            f"--output={requirements.name}",
            external=True,
        )
        session.install(f"--constraint={requirements.name}", *args, **kwargs)


@nox.session(python=["3.10"])
def tests(session):
    session.run("poetry", "install", external=True)
    session.run("pytest", "--cov")


@nox.session(python="3.10")
def black(session):
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)


@nox.session(python="3.10")
def lint(session):
    args = session.posargs or locations
    session.install("flake8", "flake8-black")
    session.run("flake8", *args)


@nox.session(python="3.10")
def mypy(session):
    args = session.posargs or locations
    session.install("mypy")
    session.run("mypy", *args)


@nox.session(python="3.10")
def safety(session):
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        session.install("safety")
        session.run("safety", "check", f"--file={requirements.name}", "--full-report")


@nox.session(python="3.10")
def pytype(session):
    """Run the static type checker."""
    args = session.posargs or ["--disable=import-error", *locations]
    session.install("pytype")
    session.run("pytype", *args)


@nox.session(python="3.10")
def docs(session: Session) -> None:
    """Build the documentation."""
    session.install("sphinx")
    session.run("sphinx-build", "docs", "docs/_build")
