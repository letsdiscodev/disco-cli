import click
import requests

from discocli import config

@click.command(name="env:set")
@click.option(
    "--project",
    required=True,
    help="the project name",
)
@click.option(
    "--disco",
    required=False,
    help="The Disco to use",
)
@click.argument(
    "variables",
    nargs=-1,
)
def env_var_set(project: str, disco: str | None, variables: list[str]) -> None:
    disco_config = config.get_disco(disco)
    click.echo(f"Setting env variable for {project}")
    url = f"https://{disco_config['host']}/.disco/projects/{project}/env"
    req_body = dict(
        envVariables=[],
    )
    for variable in variables:
        parts = variable.split("=")
        project = parts[0]
        value = "=".join(parts[1:])
        if value[0] == value[-1]:
            if value[0] in ["'", '"']:
                # remove quotes if any
                value = value[1:-1]
        req_body["envVariables"].append(dict(name=parts[0], value=value))
    response = requests.post(url,
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
    click.echo("Set")
    # TODO if deployment is not None, follow deployment