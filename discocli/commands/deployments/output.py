import json

import click
import requests
import sseclient

from discocli import config


@click.command(name="deploy:output")
@click.option(
    "--project",
    required=True,
    help="the project name",
)
@click.option(
    "--deployment",
    required=True,
    help="the deployment number",
)
@click.option(
    "--disco",
    required=False,
    help="The Disco to use",
)
def deploy_output(
    project: str, deployment: int, disco: str | None
) -> None:
    disco_config = config.get_disco(disco)
    url = f"https://{disco_config['host']}/.disco/projects/{project}/deployments/{deployment}/output"
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
