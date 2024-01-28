import click
import requests

from discocli import config

@click.command(name="syslog:remove")
@click.option(
    "--disco-domain",
    required=False,
    help="The domain where Disco is running",
)
@click.argument(
    "url",
)
def syslog_remove(url: str, disco_domain: str | None) -> None:
    disco_domain_config = config.get_disco_domain(disco_domain)
    disco_domain = disco_domain_config["domain"]
    click.echo(f"Removing Syslog URL")
    request_url = f"https://{disco_domain}/syslog"
    req_body = dict(
        action="remove",
        url=url,
    )
    response = requests.post(request_url,
        json=req_body,
        auth=(disco_domain_config["apiKey"], ""),
        headers={"Accept": "application/json"},
    )
    if response.status_code != 200:
        click.echo("Error")
        click.echo(response.text)
    resp_body = response.json()
    click.echo("Removed.")
    if len(resp_body["urls"]) > 0:
        click.echo("Current Syslog URLs:")
        for url in resp_body["urls"]:
            click.echo(url)
    else:
        click.echo("There is currently no Syslog URL set.")