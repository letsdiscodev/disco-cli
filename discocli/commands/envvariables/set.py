import json

import click
import requests
import sseclient

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
    url = f"https://{disco_config['host']}/.disco/projects/{project}/env"
    req_body = {
        "envVariables": [],
    }
    for variable in variables:
        parts = variable.split("=")
        var_name = parts[0]
        value = "=".join(parts[1:])
        if value[0] == value[-1]:
            if value[0] in ["'", '"']:
                # remove quotes if any
                value = value[1:-1]
        req_body["envVariables"].append(dict(name=var_name, value=value))
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
    if resp_body["deployment"] is not None:
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
