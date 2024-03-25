import click

from discocli.commands.init import init
from discocli.commands.meta.info import meta_info
from discocli.commands.meta.upgrade import meta_upgrade
from discocli.commands.projects.add import projects_add
from discocli.commands.projects.list import projects_list
from discocli.commands.projects.remove import projects_remove
from discocli.commands.projects.move import projects_move
from discocli.commands.deployments.deploy import deploy
from discocli.commands.deployments.list import deploy_list
from discocli.commands.deployments.output import deploy_output
from discocli.commands.commandruns.run import run
from discocli.commands.commandruns.command import command
from discocli.commands.envvariables.set import env_var_set
from discocli.commands.envvariables.get import env_var_get
from discocli.commands.envvariables.remove import env_var_remove
from discocli.commands.envvariables.list import env_var_list
from discocli.commands.logs import logs
from discocli.commands.syslog.add import syslog_add
from discocli.commands.syslog.remove import syslog_remove
from discocli.commands.syslog.list import syslog_list
from discocli.commands.nodes.add import nodes_add
from discocli.commands.scale.scale import scale


@click.group()
@click.version_option(
    package_name="disco-cli",
    message="%(package)s %(version)s",
)
def main() -> None:
    pass


main.add_command(init)
main.add_command(meta_info)
main.add_command(meta_upgrade)
main.add_command(projects_add)
main.add_command(projects_remove)
main.add_command(projects_move)
main.add_command(projects_list)
main.add_command(deploy)
main.add_command(deploy_list)
main.add_command(deploy_output)
main.add_command(run)
main.add_command(env_var_set)
main.add_command(env_var_get)
main.add_command(env_var_remove)
main.add_command(env_var_list)
main.add_command(logs)
main.add_command(syslog_add)
main.add_command(syslog_remove)
main.add_command(syslog_list)
main.add_command(command)
main.add_command(nodes_add)
main.add_command(scale)
