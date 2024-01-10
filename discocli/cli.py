import click

from discocli.commands.init import init
from discocli.commands.projects.add import projects_add
from discocli.commands.projects.list import projects_list
from discocli.commands.deployments.deploy import deploy
from discocli.commands.envvariables.set import env_var_set
from discocli.commands.envvariables.get import env_var_get
from discocli.commands.envvariables.delete import env_var_delete
from discocli.commands.envvariables.list import env_var_list


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
main.add_command(env_var_set)
main.add_command(env_var_get)
main.add_command(env_var_delete)
main.add_command(env_var_list)
