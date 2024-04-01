import click
import requests

from discocli import config

@click.command(name="apikeys:list")
@click.option(
    "--disco",
    required=False,
    help="The Disco to use",
)
def apikeys_list(disco: str | None) -> None:
    disco_config = config.get_disco(disco)
    url = f"https://{disco_config['host']}/.disco/api-keys"
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
    click.echo("Public                           Private                          Name")
    for api_key in resp_body["apiKeys"]:
        click.echo(f"{api_key['publicKey']} {api_key['privateKey']} {api_key['name']}")
