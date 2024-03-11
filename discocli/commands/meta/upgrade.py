from typing import Any
import click
import requests

from discocli import config


@click.command(name="meta:upgrade")
@click.option(
    "--image",
    required=False,
    help="the image to use. Defaults to letsdiscodev/daemon:latest",
)
@click.option(
    "--dont-pull",
    is_flag=True,
    default=False,
    help="Pull image ",
)
@click.option(
    "--disco",
    required=False,
    help="The Disco to use",
)
def meta_upgrade(
    image: str | None, dont_pull: bool, disco: str | None
) -> None:
    disco_config = config.get_disco(disco)
    url = f"https://{disco_config['host']}/.disco/disco/upgrade"
    req_body: dict[str, Any] = dict(
        pull=not dont_pull,
    )
    if image is not None:
        req_body["image"] = image
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
    click.echo("Upgrading")