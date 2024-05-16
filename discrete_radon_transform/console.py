import click
import textwrap
import requests

# from discrete_radon_transform.__init__ import __version__
from . import __version__

API_URL = "https://en.wikipedia.org/api/rest_v1/page/random/summary"


@click.command()
def wiki():
    """Client for the Wikipedia REST API, version 1."""
    with requests.get(API_URL) as response:
        response.raise_for_status()
        data = response.json()

    title = data["title"]
    extract = data["extract"]

    click.secho(title, fg="green")
    click.echo(textwrap.fill(extract))


"""Command-line interface."""


@click.command()
@click.version_option(version=__version__)
def main():
    """Discrete Radon Tranfsorm for straight lines detection."""
    click.echo("discrete radon transform for straight lines detection")
