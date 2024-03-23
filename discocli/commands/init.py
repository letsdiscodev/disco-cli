import re
import subprocess
import socket

import click

from discocli.config import add_disco

INIT_SCRIPT_URL = "https://downloads.letsdisco.dev/{version}/init"


@click.command()
@click.argument(
    "ssh",
    required=True,
)
@click.option(
    "--version",
    required=False,
    help="The version to install",
)
def init(ssh: str, version: str | None) -> None:
    if version is None:
        version = "latest"
    init_script_url = INIT_SCRIPT_URL.format(version=version)
    click.echo(f"Installing Disco on {ssh}")
    _, host = ssh.split("@")
    ip = socket.gethostbyname(host)
    command = (
        f"curl {init_script_url} | "
        f"sudo DISCO_IP={ip} DISCO_VERBOSE='false' sh"
    )
    success, output = _ssh_command(connection_str=ssh, command=command)
    if not success:
        click.echo("Failed")
        return
    else:
        api_key = _extract_api_key(output)
        public_key = _extract_ca_public_key(output)
        add_disco(name=host, host=host, ip=ip, api_key=api_key, public_key=public_key)
        click.echo("Success")
        return


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


def _extract_api_key(output: str) -> str:
    match = re.search(r"Created API key: (?P<api_key>[a-z0-9]{32})", output)
    api_key = match.group("api_key")
    return api_key

def _extract_ca_public_key(output: str) -> str:
    match = re.search(
        "-----BEGIN CERTIFICATE-----\n.*\n-----END CERTIFICATE-----", 
        output,
        re.DOTALL,
    )
    public_key = match.group(0)
    return public_key