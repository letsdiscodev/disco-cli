import click
import requests

from discocli import config

@click.command(name="env:unset")
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
@click.argument(
    "variable",
)
def env_var_delete(name: str, disco_domain: str | None, variable: str) -> None:
    disco_domain_config = config.get_disco_domain(disco_domain)
    disco_domain = disco_domain_config["domain"]
    click.echo(f"Deploying {name}")
    url = f"https://{disco_domain}/projects/{name}/env/{variable}"
    response = requests.delete(url,
        auth=(disco_domain_config["apiKey"], ""),
        headers={"Accept": "application/json"},
    )
    if response.status_code != [204, 404]:
        click.echo("Error")
        click.echo(response.text)
        return
    resp_body = response.json()
    click.echo(f"Deployed {name}, version {resp_body['deployment']['number']}")
