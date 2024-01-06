import subprocess

import click

def _ssh_command(connection_str: str, command: str, verbose: bool) -> tuple[bool, str]:
    try:
        args = [
            "ssh",
            "-vvv",
            connection_str,
            "bash -s",
        ]
        if not verbose:
            args.remove("-vvv")
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


def add_command(ssh: str, verbose: bool) -> None:
    click.echo(f"Adding project using SSH {ssh}")
    command = """docker run \
        --network=disco-network \
        disco/disco-daemon \
        curl disco-daemon:6543/
    """
    success, output = _ssh_command(connection_str=ssh, command=command, verbose=verbose)
    if not success:
        click.echo(output)
        click.echo("Failed")
        return
    else:
        click.echo(output)
        click.echo("Success")
        return
