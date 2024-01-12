import click
import requests

from discocli import config

@click.command(name="volumes:list")
@click.option(
    "--disco-domain",
    required=False,
    help="The domain where Disco is running",
)
def volumes_list(disco_domain: str | None) -> None:
    disco_domain_config = config.get_disco_domain(disco_domain)
    disco_domain = disco_domain_config["domain"]
    click.echo(f"Getting volumes")
    url = f"https://{disco_domain}/volumes"
    response = requests.get(url,
        auth=(disco_domain_config["apiKey"], ""),
        headers={"Accept": "application/json"},
    )
    if response.status_code != 200:
        click.echo("Error")
        click.echo(response.text)
    click.echo("Volumes:")
    for volume in response.json()["volumes"]:
        click.echo(volume["name"])
