import click

@click.group()
@click.version_option(
    package_name="disco-cli",
    message="%(package)s %(version)s",
)
def main():
    pass

@main.command()
@click.option(
    "--ssh",
    required=True,
    help="user@host, e.g. root@123.123.123.123",
)
def init(ssh: str):
    click.echo(f"Would connect to {ssh} and init.")
