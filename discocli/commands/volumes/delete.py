import click
import requests

from discocli import config

@click.command(name="volumes:delete")
@click.option(
    "--name",
    required=True,
    help="the name of the volume",
)
@click.option(
    "--disco-domain",
    required=False,
    help="The domain where Disco is running",
)
def volumes_delete(name: str, disco_domain: str | None) -> None:
    disco_domain_config = config.get_disco_domain(disco_domain)
    disco_domain = disco_domain_config["domain"]
    click.echo(f"Deleting volume")
    url = f"https://{disco_domain}/volumes/{name}"
    response = requests.delete(url,
        auth=(disco_domain_config["apiKey"], ""),
        headers={"Accept": "application/json"},
    )
    if response.status_code != 204:
        click.echo("Error")
        click.echo(response.text)
        return
