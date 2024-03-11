import click
import requests

from discocli import config

@click.command(name="meta:info")
@click.option(
    "--disco",
    required=False,
    help="The Disco to use",
)
def meta_info(disco: str | None) -> None:
    disco_config = config.get_disco(disco)
    url = f"https://{disco_config['host']}/.disco/disco/meta"
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
    click.echo(f"Version:         {resp_body['version']}")
    click.echo(f"IP address:      {resp_body['ip']}")
    click.echo(f"Disco Host:      {resp_body['discoHost']}")
    click.echo(f"Registry Host:   {resp_body['registryHost']}")
