import subprocess
import click
import requests

from discocli import config

NODE_SCRIPT_URL = "https://downloads.letsdisco.dev/{version}/node"

@click.command(name="nodes:add")
@click.option(
    "--disco",
    required=False,
    help="The Disco to use",
)
@click.option(
    "--version",
    required=False,
    help="The version to install",
)
@click.argument(
    "ssh",
    required=True,
)
def nodes_add(
    disco: str | None, ssh: str, version: str | None
) -> None:
    if version is None:
        version = "latest"
    node_script_url = NODE_SCRIPT_URL.format(version=version)
    disco_config = config.get_disco(disco)
    url = f"https://{disco_config['host']}/.disco/disco/swarm/join-token"
    response = requests.get(
        url,
        auth=(disco_config["apiKey"], ""),
        headers={"Accept": "application/json"},
        verify=config.requests_verify(disco_config),
    )
    if response.status_code != 200:
        click.echo("Error")
        click.echo(response.text)
        return
    resp_body = response.json()
    token = resp_body["joinToken"]
    ip = resp_body["ip"]
    command = (
        f"curl {node_script_url} | "
        f"sudo IP={ip} TOKEN={token} sh"
    )
    success, output = _ssh_command(connection_str=ssh, command=command)
    


def _ssh_command(connection_str: str, command: str) -> tuple[bool, str]:
    args = [
        "ssh",
        connection_str,
        command,
    ]
    process = subprocess.Popen(
        args=args,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    output = ""
    assert process.stdout is not None
    for line in process.stdout:
        print(line.decode("utf-8"), end="")
        output += line.decode("utf-8")
    process.wait()
    return process.returncode == 0, output
