import re
import click
import requests

from discocli import config

@click.command(name="projects:remove")
@click.option(
    "--disco",
    required=False,
    help="The Disco to use",
)
@click.argument(
    "project",
)
def projects_remove(project: str, disco: str | None) -> None:
    disco_config = config.get_disco(disco)
    click.echo(f"Removing project...")
    url = f"https://{disco_config['host']}/.disco/projects/{project}"
    response = requests.delete(url,
        auth=(disco_config["apiKey"], ""),
        headers={"Accept": "application/json"},
        verify=config.requests_verify(disco_config),
    )
    if response.status_code not in [200, 204]:
        click.echo("Error")
        click.echo(response.text)
        return
    click.echo("Project removed.")
