import re
import click
import requests

from discocli import config

@click.command(name="apikeys:remove")
@click.option(
    "--disco",
    required=False,
    help="The Disco to use",
)
@click.argument(
    "public_key",
)
def apikeys_remove(public_key: str, disco: str | None) -> None:
    disco_config = config.get_disco(disco)
    url = f"https://{disco_config['host']}/.disco/api-keys/{public_key}"
    response = requests.delete(url,
        auth=(disco_config["apiKey"], ""),
        headers={"Accept": "application/json"},
        verify=config.requests_verify(disco_config),
    )
    if response.status_code not in [200, 204]:
        click.echo("Error")
        click.echo(response.text)
        return
