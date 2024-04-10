import re
import click
import requests

from discocli import config


@click.command(name="invite:create")
@click.option(
    "--disco",
    required=False,
    help="The Disco to use",
)
@click.argument(
    "name",
    required=True,
)
def invite_create(
    name: str, disco: str | None
) -> None:
    disco_config = config.get_disco(disco)
    url = f"https://{disco_config['host']}/.disco/api-key-invites"
    req_body = dict(
        name=name,
    )
    response = requests.post(
        url,
        json=req_body,
        auth=(disco_config["apiKey"], ""),
        headers={"Accept": "application/json"},
        verify=config.requests_verify(disco_config),
    )
    if response.status_code != 201:
        click.echo("Error")
        click.echo(response.text)
        return
    resp_body = response.json()
    click.echo("Send this link to the new user:")
    click.echo(resp_body["apiKeyInvite"]["url"])