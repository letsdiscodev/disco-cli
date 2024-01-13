import click
import requests

from discocli import config

@click.command(name="volumes:detach")
@click.option(
    "--volume",
    required=True,
    help="the name of the volume",
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
def volumes_detach(volume: str, project: str, disco_domain: str | None) -> None:
    disco_domain_config = config.get_disco_domain(disco_domain)
    disco_domain = disco_domain_config["domain"]
    click.echo(f"Detaching volume")
    url = f"https://{disco_domain}/volumes/{volume}/attachments/{project}"
    response = requests.delete(url,
        auth=(disco_domain_config["apiKey"], ""),
        headers={"Accept": "application/json"},
    )
    if response.status_code != 201:
        click.echo("Error")
        click.echo(response.text)
    resp_body = response.json()
    click.echo("Detached")
    if resp_body["deployment"] is not None:
        click.echo(f"Deploying {project}, version {resp_body['deployment']['number']}")
