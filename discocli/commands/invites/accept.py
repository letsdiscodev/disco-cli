import re
import click
import requests
import sseclient
import json

from discocli import config


@click.command(name="invite:accept")
@click.option(
    "--show-only",
    is_flag=True,
    default=False,
    help="Show new API key only without updating CLI config",
)
@click.argument(
    "url",
    required=True,
)
def invite_accept(
    url: str,
    show_only: bool
) -> None:
    response = requests.post(
        url,
        headers={"Accept": "application/json"},
    )
    if response.status_code != 200:
        click.echo("Error")
        click.echo(response.text)
        return
    resp_body = response.json()
    if config.disco_already_in_config(resp_body["meta"]["discoHost"]):
        show_only = True
        click.echo(f"{resp_body['meta']['discoHost']} already in config, here's your new API key:")
    if show_only:
        click.echo("")
        click.echo(f"Private Key: {resp_body['apiKey']['privateKey']}")
        click.echo(f"Public Key:  {resp_body['apiKey']['publicKey']}")
        click.echo(f"Host:        {resp_body['meta']['discoHost']}")
        click.echo(f"IP:          {resp_body['meta']['ip']}")
    else:
        config.add_disco(
            name=resp_body["meta"]["discoHost"],
            host=resp_body["meta"]["discoHost"],
            ip=resp_body["meta"]["ip"],
            api_key=resp_body["apiKey"]["privateKey"],
        )