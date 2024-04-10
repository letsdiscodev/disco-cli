import click
import requests

from discocli import config

@click.command(name="scale")
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
    "services",
    nargs=-1,
)
def scale(project: str, disco: str | None, services: list[str]) -> None:
    disco_config = config.get_disco(disco)
    url = f"https://{disco_config['host']}/.disco/projects/{project}/scale"
    req_body: dict[str, dict[str, int]] = {"services": {}}
    for service in services:
        parts = service.split("=")
        service_name = parts[0]
        replicas = parts[1]
        req_body["services"][service_name] = int(replicas)
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
