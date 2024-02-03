import re
import subprocess

import click

from discocli.config import set_api_key

INIT_SCRIPT_URL = "https://downloads.letsdisco.dev/latest/init"


@click.command()
@click.option(
    "--ssh",
    required=True,
    help="user@host, e.g. root@123.123.123.123",
)
@click.option(
    "--disco-domain",
    required=True,
    help="domain name where disco will be served, e.g. disco.example.com",
)
def init(ssh: str, disco_domain: str) -> None:
    click.echo(f"Installing Disco on {ssh}")
    _, disco_ip = ssh.split("@")
    command = (
        f"curl {INIT_SCRIPT_URL} | "
        f"sudo DISCO_DOMAIN={disco_domain} DISCO_IP={disco_ip} sh"
    )
    success, output = _ssh_command(connection_str=ssh, command=command)
    if not success:
        click.echo("Failed")
        return
    else:
        api_key = _extract_api_key(output)
        set_api_key(disco_domain=disco_domain, api_key=api_key)
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
    for line in process.stdout:
        print(line.decode("utf-8"), end="")
        output += line.decode("utf-8")
    process.wait()
    return process.returncode == 0, output


def _extract_api_key(output: str) -> str:
    match = re.search(r"Created API key: (?P<api_key>[a-z0-9]{32})", output)
    api_key = match.group("api_key")
    return api_key
