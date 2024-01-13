import click

from discocli.commands.init import init
from discocli.commands.projects.add import projects_add
from discocli.commands.projects.list import projects_list
from discocli.commands.deployments.deploy import deploy
from discocli.commands.envvariables.set import env_var_set
from discocli.commands.envvariables.get import env_var_get
from discocli.commands.envvariables.delete import env_var_delete
from discocli.commands.envvariables.list import env_var_list
from discocli.commands.volumes.add import volumes_add
from discocli.commands.volumes.list import volumes_list
from discocli.commands.volumes.delete import volumes_delete
from discocli.commands.volumes.attach import volumes_attach
from discocli.commands.volumes.detach import volumes_detach
from discocli.commands.publishedports.add import publishedports_add
from discocli.commands.publishedports.remove import publishedports_remove


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
main.add_command(volumes_add)
main.add_command(volumes_list)
main.add_command(volumes_delete)
main.add_command(volumes_attach)
main.add_command(volumes_detach)
main.add_command(publishedports_add)
main.add_command(publishedports_remove)
