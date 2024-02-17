import click
import requests

from discocli import config

@click.command(name="syslog:add")
@click.option(
    "--disco",
    required=False,
    help="The Disco to use",
)
@click.argument(
    "url",
)
def syslog_add(url: str, disco: str | None) -> None:
    disco_config = config.get_disco(disco)
    click.echo(f"Adding Syslog URL")
    request_url = f"https://{disco_config['host']}/.disco/syslog"
    req_body = dict(
        action="add",
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
    click.echo("Added.")
    if len(resp_body["urls"]) > 0:
        click.echo("Current Syslog URLs:")
        for url in resp_body["urls"]:
            click.echo(url)
    else:
        click.echo("There is currently no Syslog URL set.")
