import click
import requests

from discocli import config

@click.command(name="env:set")
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
    "variables",
    nargs=-1,
)
def env_var_set(name: str, disco_domain: str | None, variables: list[str]) -> None:
    disco_domain_config = config.get_disco_domain(disco_domain)
    disco_domain = disco_domain_config["domain"]
    click.echo(f"Setting env variable for {name}")
    url = f"https://{disco_domain}/projects/{name}/env"
    req_body = dict(
        envVariables=[],
    )
    for variable in variables:
        parts = variable.split("=")
        name = parts[0]
        value = "=".join(parts[1:])
        if value[0] == value[-1]:
            if value[0] in ["'", '"']:
                # remove quotes if any
                value = value[1:-1]
        req_body["envVariables"].append(dict(name=parts[0], value=value))
    response = requests.post(url,
        json=req_body,
        auth=(disco_domain_config["apiKey"], ""),
        headers={"Accept": "application/json"},
    )
    if response.status_code != 200:
        click.echo("Error")
        click.echo(response.text)
        return
    resp_body = response.json()
    click.echo("Set")
    if resp_body["deployment"] is not None:
        click.echo(f"Deployed {name}, version {resp_body['deployment']['number']}")
