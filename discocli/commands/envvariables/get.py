import click
import requests

from discocli import config

@click.command(name="env:get")
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
def env_var_get(project: str, disco: str | None, variable: str) -> None:
    disco_config = config.get_disco(disco)
    click.echo(f"Fetching env variable for {project}: {variable}")
    url = f"https://{disco_config['host']}/.disco/projects/{project}/env/{variable}"
    response = requests.get(url,
        auth=(disco_config["apiKey"], ""),
        headers={"Accept": "application/json"},
        verify=config.requests_verify(disco_config),
    )
    if response.status_code == 404:
        click.echo("")
        return
    if response.status_code != 200:
        click.echo("Error")
        click.echo(response.text)
        return
    resp_body = response.json()
    click.echo(resp_body["envVariable"]["value"])
