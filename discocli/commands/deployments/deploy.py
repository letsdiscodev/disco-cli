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
    "--commit",
    required=False,
    help="the commit to deploy, e.g. 7b5c8f935328c1af49c9037cac9dee7bf0bd8c7e",
)
@click.option(
    "--file",
    required=False,
    help="the JSON file to deploy",
)
@click.option(
    "--disco-domain",
    required=False,
    help="The domain where Disco is running",
)
def deploy(name: str, commit: str, file: str, disco_domain: str | None) -> None:
    disco_domain_config = config.get_disco_domain(disco_domain)
    disco_domain = disco_domain_config["domain"]
    click.echo(f"Deploying {name}")
    url = f"https://{disco_domain}/projects/{name}/deployments"
    disco_config = None
    if file is not None:
        with open(file, "r", encoding="utf-8") as f:
            disco_config = f.read()
    req_body = dict(
        commit=commit,
        discoConfig=disco_config,
    )
    response = requests.post(url,
        json=req_body,
        auth=(disco_domain_config["apiKey"], ""),
        headers={"Accept": "application/json"},
    )
    if response.status_code != 201:
        click.echo("Error")
        click.echo(response.text)
    resp_body = response.json()
    click.echo(f"Deployed {name}, version {resp_body['deployment']['number']}")
