import click
import requests

from discocli import config

@click.command(name="volumes:add")
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
def volumes_add(name: str, disco_domain: str | None) -> None:
    disco_domain_config = config.get_disco_domain(disco_domain)
    disco_domain = disco_domain_config["domain"]
    click.echo(f"Creating volume")
    url = f"https://{disco_domain}/volumes"
    req_body = dict(
        name=name,
    )
    response = requests.post(url,
        json=req_body,
        auth=(disco_domain_config["apiKey"], ""),
        headers={"Accept": "application/json"},
    )
    if response.status_code != 201:
        click.echo("Error")
        click.echo(response.text)
