import click
import requests

from discocli import config

@click.command(name="deploy:list")
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
def deploy_list(project: str, disco: str | None) -> None:
    disco_config = config.get_disco(disco)
    url = f"https://{disco_config['host']}/.disco/projects/{project}/deployments"
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
    for deployment in resp_body["deployments"]:
        click.echo(f"{deployment['created']}\t{deployment['number']}\t{deployment['status']}")
