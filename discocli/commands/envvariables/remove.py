import click
import requests

from discocli import config

@click.command(name="env:unset")
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
@click.argument(
    "variable",
)
def env_var_remove(project: str, disco: str | None, variable: str) -> None:
    disco_config = config.get_disco(disco)
    click.echo(f"Removing env variable from {project}")
    url = f"https://{disco_config['host']}/.disco/projects/{project}/env/{variable}"
    response = requests.delete(url,
        auth=(disco_config["apiKey"], ""),
        headers={"Accept": "application/json"},
        verify=config.requests_verify(disco_config),
    )
    if response.status_code != [204, 404]:
        click.echo("Error")
        click.echo(response.text)
        return
    # TODO some confirmation output
    # TODO if deployment is not None, follow deployment