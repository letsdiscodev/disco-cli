import click
import requests

from discocli import config

@click.command(name="syslog:remove")
@click.option(
    "--disco",
    required=False,
    help="The Disco to use",
)
@click.argument(
    "url",
)
def syslog_remove(url: str, host: str | None) -> None:
    disco_config = config.get_disco(host)
    click.echo(f"Removing Syslog URL")
    request_url = f"https://{disco_config['host']}/.disco/syslog"
    req_body = dict(
        action="remove",
        url=url,
    )
    response = requests.post(request_url,
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
    click.echo("Removed.")
    if len(resp_body["urls"]) > 0:
        click.echo("Current Syslog URLs:")
        for url in resp_body["urls"]:
            click.echo(url)
    else:
        click.echo("There is currently no Syslog URL set.")
