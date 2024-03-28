import sys
import click
import requests

from discocli import config


@click.command(name="volumes:list")
@click.option(
    "--project",
    required=True,
    help="the project name",
)
@click.option(
    "--disco",
    required=False,
    help="The Disco to use",
)
def volumes_list(project: str, disco: str | None) -> None:
    disco_config = config.get_disco(disco)
    url = f"https://{disco_config['host']}/.disco/projects/{project}/volumes"
    response = requests.get(
        url,
        auth=(disco_config["apiKey"], ""),
        headers={"Accept": "application/json"},
        verify=config.requests_verify(disco_config),
    )
    if response.status_code != 200:
        click.echo("Error", err=True)
        click.echo(response.text, err=True)
        return
    for volume in response.json()["volumes"]:
        click.echo(volume["name"])
