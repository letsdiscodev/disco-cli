import sys
import click
import requests

from discocli import config


@click.command(name="volumes:import")
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
@click.option(
    "--volume",
    required=True,
    help="the volume name as seen in your disco.json file",
)
def volumes_import(project: str, disco: str | None, volume: str) -> None:
    disco_config = config.get_disco(disco)
    url = f"https://{disco_config['host']}/.disco/projects/{project}/volumes/{volume}"
    response = requests.put(
        url,
        data=sys.stdin.buffer,
        auth=(disco_config["apiKey"], ""),
        headers={"Accept": "application/json"},
        verify=config.requests_verify(disco_config),
    )
    if response.status_code != 200:
        click.echo("Error", err=True)
        click.echo(response.text, err=True)
        return
