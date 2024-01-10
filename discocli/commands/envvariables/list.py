import click
import requests

from discocli import config

@click.command(name="env:list")
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
def env_var_list(name: str, disco_domain: str | None) -> None:
    disco_domain_config = config.get_disco_domain(disco_domain)
    disco_domain = disco_domain_config["domain"]
    click.echo(f"Fetching env variables for {name}")
    url = f"https://{disco_domain}/projects/{name}/env"
    response = requests.get(url,
        auth=(disco_domain_config["apiKey"], ""),
        headers={"Accept": "application/json"},
    )
    if response.status_code == 404:
        click.echo("")
        return
    if response.status_code != 200:
        click.echo("Error")
        click.echo(response.text)
        return
    resp_body = response.json()
    for variable in resp_body["envVariables"]:
        click.echo(f"{variable['name']}={variable['value']}")
