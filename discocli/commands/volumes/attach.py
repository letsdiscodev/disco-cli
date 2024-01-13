import click
import requests

from discocli import config

@click.command(name="volumes:attach")
@click.option(
    "--volume",
    required=True,
    help="the name of the volume",
)
@click.option(
    "--destination",
    required=True,
    help="the path to mount the volume in the project",
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
def volumes_attach(volume: str, destination: str, project: str, disco_domain: str | None) -> None:
    disco_domain_config = config.get_disco_domain(disco_domain)
    disco_domain = disco_domain_config["domain"]
    click.echo(f"Attaching volume")
    url = f"https://{disco_domain}/volumes/{volume}/attachments/{project}"
    req_body = dict(
        destination=destination,
    )
    response = requests.post(url,
        json=req_body,
        auth=(disco_domain_config["apiKey"], ""),
        headers={"Accept": "application/json"},
    )
    if response.status_code != 200:
        click.echo("Error")
        click.echo(response.text)
    resp_body = response.json()
    click.echo("Attached")
    if resp_body["deployment"] is not None:
        click.echo(f"Deploying {project}, version {resp_body['deployment']['number']}")
