import json
import click
import requests
import sseclient

from discocli import config

@click.command(name="logs")
@click.option(
    "--project",
    required=False,
    help="The project you want to get logs about",
)
@click.option(
    "--service",
    required=False,
    help="The service you want to get logs about",
)
@click.option(
    "--disco",
    required=False,
    help="The Disco to use",
)
def logs(disco: str | None, project: str | None, service: str | None) -> None:
    disco_config = config.get_disco(disco)
    if project is None and service is not None:
        raise Exception("Must specify project when specifying service")
    url = f"https://{disco_config['host']}/.disco/logs"
    if project is not None:
        url = f"{url}/{project}" 
    if service is not None:
        url = f"{url}/{service}" 
    response = requests.get(url,
        auth=(disco_config["apiKey"], ""),
        headers={'Accept': 'text/event-stream'},
        stream=True,
        verify=config.requests_verify(disco_config),
    )
    if response.status_code == 404:
        click.echo("Not found")
        return
    for event in sseclient.SSEClient(response).events():
        log_item = json.loads(event.data)
        if "com.docker.swarm.service.name" not in log_item["labels"]:
            continue
        container = log_item["container"][1:]
        timestamp = log_item["timestamp"]
        message = log_item["message"]
        click.echo(f"{container} {timestamp} {message}")
