import json

import click
import requests
import sseclient

from discocli import config


@click.command(name="run")
@click.option(
    "--project",
    required=True,
    help="the project name",
)
@click.option(
    "--service",
    required=False,
    help="The service you want to use to run the command",
)
@click.option(
    "--timeout",
    required=False,
    help="The timeout in seconds for the command before it's killed",
    default=600,
)
@click.option(
    "--disco",
    required=False,
    help="The Disco to use",
)
@click.argument(
    "command",
)
def run(
    project: str, service: str, command: str, timeout: int, disco: str | None
) -> None:
    disco_config = config.get_disco(disco)
    url = f"https://{disco_config['host']}/.disco/projects/{project}/runs"
    req_body = dict(
        command=command,
        service=service,
        timeout=timeout,
    )
    response = requests.post(
        url,
        json=req_body,
        auth=(disco_config["apiKey"], ""),
        headers={"Accept": "application/json"},
        verify=config.requests_verify(disco_config),
    )
    if response.status_code != 202:
        click.echo("Error")
        click.echo(response.text)
        return
    resp_body = response.json()
    url = f"https://{disco_config['host']}/.disco/projects/{project}/runs/{resp_body['run']['number']}/output"
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
