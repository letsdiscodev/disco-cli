import click
import requests

from discocli import config

@click.command(name="published-ports:add")
@click.option(
    "--host-port",
    required=True,
    type=int,
    help="the port on the host that will be public on the machine",
)
@click.option(
    "--container-port",
    required=True,
    type=int,
    help="the port on the container you want to publis on the host",
)
@click.option(
    "--protocol",
    required=True,
    help="the protocol, e.g. tcp or udp",
)
@click.option(
    "--project",
    required=True,
    help="the name of the project",
)
@click.option(
    "--disco-domain",
    required=False,
    help="The domain where Disco is running",
)
def publishedports_add(host_port: int, container_port: int, protocol: str, project: str, disco_domain: str | None) -> None:
    disco_domain_config = config.get_disco_domain(disco_domain)
    disco_domain = disco_domain_config["domain"]
    click.echo(f"Adding published port")
    url = f"https://{disco_domain}/projects/{project}/published-ports"
    req_body = dict(
        hostPort=host_port,
        containerPort=container_port,
        protocol=protocol,
    )
    response = requests.post(url,
        json=req_body,
        auth=(disco_domain_config["apiKey"], ""),
        headers={"Accept": "application/json"},
    )
    if response.status_code != 201:
        click.echo("Error")
        click.echo(response.text)
    resp_body = response.json()
    click.echo("Added published port")
    if resp_body["deployment"] is not None:
        click.echo(f"Deploying {project}, version {resp_body['deployment']['number']}")
