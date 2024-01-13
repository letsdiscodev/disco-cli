import click
import requests

from discocli import config

@click.command(name="published-ports:remove")
@click.option(
    "--host-port",
    required=True,
    type=int,
    help="the port on the host that will be public on the machine",
)
@click.option(
    "--project",
    required=True,
    help="the name of the project",
)
@click.option(
    "--disco-domain",
    required=False,
    help="The domain where Disco is running",
)
def publishedports_remove(host_port: int, project: str, disco_domain: str | None) -> None:
    disco_domain_config = config.get_disco_domain(disco_domain)
    disco_domain = disco_domain_config["domain"]
    click.echo(f"Removing published port")
    url = f"https://{disco_domain}/projects/{project}/published-ports/{host_port}"
    response = requests.delete(url,
        auth=(disco_domain_config["apiKey"], ""),
        headers={"Accept": "application/json"},
    )
    if response.status_code != 200:
        click.echo("Error")
        click.echo(response.text)
    resp_body = response.json()
    click.echo("Removed published port")
    if resp_body["deployment"] is not None:
        click.echo(f"Deploying {project}, version {resp_body['deployment']['number']}")
