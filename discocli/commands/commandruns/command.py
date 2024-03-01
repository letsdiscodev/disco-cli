import json

import click
import requests
import sseclient

from discocli import config

@click.command(name="command", context_settings=dict(
    ignore_unknown_options=True,
))
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
    "project",
)
@click.argument(
    "command",
)
@click.argument(
    "args",
    nargs=-1,
)
def command(project: str, command: str, args: str, timeout: int, disco: str | None) -> None:
    disco_config = config.get_disco(disco)
    click.echo(f"Running command...")
    url = f"https://{disco_config['host']}/.disco/projects/{project}/runs"
    req_body = dict(
        command=" ".join(args),
        service=command,
        timeout=timeout,
    )
    response = requests.post(url,
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
    response = requests.get(url,
        auth=(disco_config["apiKey"], ""),
        headers={'Accept': 'text/event-stream'},
        stream=True,
        verify=config.requests_verify(disco_config),
    )
    for event in sseclient.SSEClient(response).events():
        output = json.loads(event.data)
        click.echo(output["text"], nl=False)

