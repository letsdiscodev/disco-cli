import click

from discocli.commands.init import init
from discocli.commands.projects.add import projects_add
from discocli.commands.projects.list import projects_list
from discocli.commands.deployments.deploy import deploy


@click.group()
@click.version_option(
    package_name="disco-cli",
    message="%(package)s %(version)s",
)
def main() -> None:
    pass


main.add_command(init)
main.add_command(projects_add)
main.add_command(projects_list)
main.add_command(deploy)
