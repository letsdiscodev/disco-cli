import click
import requests

from discocli import config


@click.command(name="meta:host")
@click.option(
    "--disco",
    required=False,
    help="The Disco to use",
)
@click.argument(
    "domain",
    required=True,
)
def meta_host(domain: str, disco: str | None) -> None:
    disco_config = config.get_disco(disco)
    url = f"https://{disco_config['host']}/.disco/disco/host"
    req_body = dict(
        host=domain,
    )
    response = requests.post(
        url,
        json=req_body,
        auth=(disco_config["apiKey"], ""),
        headers={"Accept": "application/json"},
        verify=config.requests_verify(disco_config),
    )
    if response.status_code != 200:
        click.echo("Error")
        click.echo(response.text)
        return
    resp_body = response.json()
    config.set_host(name=disco_config["name"], host=resp_body["discoHost"])
