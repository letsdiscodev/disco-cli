import click
import requests

from discocli import config

@click.command(name="projects:list")
@click.option(
    "--disco",
    required=False,
    help="The Disco to use",
)
def projects_list(disco: str | None) -> None:
    disco_config = config.get_disco(disco)
    click.echo(f"Listing projects")
    url = f"https://{disco_config['host']}/.disco/projects"
    response = requests.get(url,
        auth=(disco_config["apiKey"], ""),
        headers={"Accept": "application/json"},
        verify=config.requests_verify(disco_config),
    )
    if response.status_code != 200:
        click.echo("Error")
        click.echo(response.text)
        return
    resp_body = response.json()
    for project in resp_body["projects"]:
        click.echo(project["name"])
        click.echo(project["githubRepo"])
        click.echo("")