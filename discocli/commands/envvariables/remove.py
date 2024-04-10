import json

import click
import requests
import sseclient

from discocli import config

@click.command(name="env:unset")
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
    "variable",
)
def env_var_remove(project: str, disco: str | None, variable: str) -> None:
    disco_config = config.get_disco(disco)
    click.echo(f"Removing env variable from {project}")
    url = f"https://{disco_config['host']}/.disco/projects/{project}/env/{variable}"
    response = requests.delete(url,
        auth=(disco_config["apiKey"], ""),
        headers={"Accept": "application/json"},
        verify=config.requests_verify(disco_config),
    )
    if response.status_code != 200:
        click.echo("Error")
        click.echo(response.text)
        return
    resp_body = response.json()
    if resp_body["deployment"] is not None:
        click.echo(f"Deploying {project}, version {resp_body['deployment']['number']}")
        url = f"https://{disco_config['host']}/.disco/projects/{project}/deployments/{resp_body['deployment']['number']}/output"
        response = requests.get(
            url,
            auth=(disco_config["apiKey"], ""),
            headers={"Accept": "text/event-stream"},
            stream=True,
            verify=config.requests_verify(disco_config),
        )
        for event in sseclient.SSEClient(response).events():
            if event.event == "output":
                output = json.loads(event.data)
                click.echo(output["text"], nl=False)
            elif event.event == "end":
                break
