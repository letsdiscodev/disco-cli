import click
import requests

from discocli import config

@click.command(name="env:list")
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
def env_var_list(project: str, disco: str | None) -> None:
    disco_config = config.get_disco(disco)
    click.echo(f"Fetching env variables for {project}")
    url = f"https://{disco_config['host']}/.disco/projects/{project}/env"
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
    for variable in resp_body["envVariables"]:
        click.echo(f"{variable['name']}={variable['value']}")
