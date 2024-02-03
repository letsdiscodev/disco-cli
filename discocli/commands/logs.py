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
    "--disco-domain",
    required=False,
    help="The domain where Disco is running",
)
def logs(disco_domain: str | None, project: str | None, service: str | None) -> None:
    disco_domain_config = config.get_disco_domain(disco_domain)
    disco_domain = disco_domain_config["domain"]
    if project is None and service is not None:
        raise Exception("Must specify project when specifying service")
    url = f"https://{disco_domain}/logs"
    if project is not None:
        url = f"{url}/{project}" 
    if service is not None:
        url = f"{url}/{service}" 
    response = requests.get(url,
        auth=(disco_domain_config["apiKey"], ""),
        headers={'Accept': 'text/event-stream'},
        stream=True,
    )
    for event in sseclient.SSEClient(response).events():
        log_item = json.loads(event.data)
        if "com.docker.swarm.service.name" not in log_item["labels"]:
            continue
        container = log_item["container"][1:]
        timestamp = log_item["timestamp"]
        message = log_item["message"]
        click.echo(f"{container} {timestamp} {message}")
