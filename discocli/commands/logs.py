import json
import click
from websockets.sync.client import connect

from discocli import config

@click.command(name="logs")
@click.option(
    "--disco-domain",
    required=False,
    help="The domain where Disco is running",
)
def logs(disco_domain: str | None) -> None:
    disco_domain_config = config.get_disco_domain(disco_domain)
    disco_domain = disco_domain_config["domain"]
    url = f"wss://{disco_domain}/logs"
    with connect(url) as websocket:
        while True:
            log_json_str = websocket.recv()
            log_item = json.loads(log_json_str)
            if "com.docker.swarm.service.name" not in log_item["labels"]:
                continue
            service = log_item["labels"]["com.docker.swarm.service.name"]
            timestamp = log_item["timestamp"]
            message = log_item["message"]
            click.echo(f"{service} {timestamp} {message}")
