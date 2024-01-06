import click



@click.group()
@click.version_option(
    package_name="disco-cli",
    message="%(package)s %(version)s",
)
def main() -> None:
    pass

@main.command()
@click.option(
    "--ssh",
    required=True,
    help="user@host, e.g. root@123.123.123.123",
)
@click.option(
    "--verbose",
    default=False,
    show_default=True,
    help="Make the operation more talkative",
)
def init(ssh: str, verbose: bool) -> None:
    from discocli.commands.init import init_command

    init_command(ssh=ssh, verbose=verbose)
