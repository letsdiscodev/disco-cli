import json

import click
import requests
import sseclient

from discocli import config


@click.command(name="deploy")
@click.option(
    "--project",
    required=True,
    help="the project name",
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
    "--disco",
    required=False,
    help="The Disco to use",
)
def deploy(
    project: str, commit: str | None, file: str | None, disco: str | None
) -> None:
    disco_config = config.get_disco(disco)
    url = f"https://{disco_config['host']}/.disco/projects/{project}/deployments"
    disco_file = None
    if file is not None:
        with open(file, "r", encoding="utf-8") as f:
            disco_file = f.read()
    req_body = dict()
    if commit is not None:
        req_body["commit"] = commit
    if disco_file is not None:
        req_body["discoFile"] = disco_file
    response = requests.post(
        url,
        json=req_body,
        auth=(disco_config["apiKey"], ""),
        headers={"Accept": "application/json"},
        verify=config.requests_verify(disco_config),
    )
    if response.status_code != 201:
        click.echo("Error")
        click.echo(response.text)
        return
    resp_body = response.json()
    url = f"https://{disco_config['host']}/.disco/projects/{project}/deployments/{resp_body['deployment']['number']}/output"
    response = requests.get(
        url,
        auth=(disco_config["apiKey"], ""),
        headers={"Accept": "text/event-stream"},
        stream=True,
        verify=config.requests_verify(disco_config),
    )
    for event in sseclient.SSEClient(response).events():
        output = json.loads(event.data)
        click.echo(output["text"], nl=False)
