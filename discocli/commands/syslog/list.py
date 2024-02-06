import click
import requests

from discocli import config

@click.command(name="syslog:list")
@click.option(
    "--disco",
    required=False,
    help="The Disco to use",
)
def syslog_list(disco: str | None) -> None:
    disco_config = config.get_disco(disco)
    click.echo(f"Getting Syslog URLs")
    url = f"https://{disco_config['host']}/.disco/syslog"
    response = requests.get(url,
        auth=(disco_config["apiKey"], ""),
        headers={"Accept": "application/json"},
        verify=config.requests_verify(disco_config),
    )
    if response.status_code != 200:
        click.echo("Error")
        click.echo(response.text)
    resp_body = response.json()
    if len(resp_body["urls"]) > 0:
        click.echo("Current Syslog URLs:")
        for url in resp_body["urls"]:
            click.echo(url)
    else:
        click.echo("There is currently no Syslog URL set.")
