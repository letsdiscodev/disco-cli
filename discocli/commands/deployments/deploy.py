import click
import requests

from discocli import config

@click.command(name="deploy")
@click.option(
    "--name",
    required=True,
    help="the name that you'll use to refer to the project",
)
@click.option(
    "--disco-domain",
    required=False,
    help="The domain where Disco is running",
)
def deploy(name: str, disco_domain: str | None) -> None:
    disco_domain_config = config.get_disco_domain(disco_domain)
    disco_domain = disco_domain_config["domain"]
    click.echo(f"Deploying {name}")
    url = f"https://{disco_domain}/projects/{name}/deployments"
    response = requests.post(url,
        auth=(disco_domain_config["apiKey"], ""),
        headers={"Accept": "application/json"},
    )
    if response.status_code != 201:
        click.echo("Error")
        click.echo(response.text)
    resp_body = response.json()
    click.echo(f"Deployed {name}, version {resp_body['deployment']['number']}")