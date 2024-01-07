import subprocess

import click

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
    command = (
        f"curl {INIT_SCRIPT_URL} | "
        f"sudo DISCO_DOMAIN={disco_domain} sh"
    )
    success, output = _ssh_command(connection_str=ssh, command=command)
    if not success:
        click.echo(output)
        click.echo("Failed")
        return
    else:
        click.echo(output)
        click.echo("Success")
        return


def _ssh_command(connection_str: str, command: str) -> tuple[bool, str]:
    try:
        args = [
            "ssh",
            connection_str,
            "bash -s",
        ]
        result = subprocess.run(
            args=args,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            input=command.encode("utf-8"),
        )
    except subprocess.CalledProcessError as ex:
        return False, ex.stdout.decode("utf-8")
    return True, result.stdout.decode("utf-8")
