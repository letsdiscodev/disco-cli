import re
import click
import requests
import sseclient
import json

from discocli import config


@click.command(name="projects:add")
@click.option(
    "--name",
    required=True,
    help="the project name",
)
@click.option(
    "--domain",
    required=False,
    help="domain name where the app will be served, e.g. www.example.com",
)
@click.option(
    "--github-repo",
    required=False,
    help="URL used to clone the repo, e.g. git@github.com:example/example.git",
)
@click.option(
    "--disco",
    required=False,
    help="The Disco to use",
)
@click.option(
    "--deploy",
    is_flag=True,
    default=False,
    help="Greet the world.",
)
def projects_add(
    name: str, domain: str, github_repo: str, disco: str | None, deploy: bool
) -> None:
    disco_config = config.get_disco(disco)
    click.echo(f"Adding project...")
    url = f"https://{disco_config['host']}/.disco/projects"
    req_body = dict(
        name=name,
        githubRepo=github_repo,
        domain=domain,
        deploy=deploy,
    )
    response = requests.post(
        url,
        json=req_body,
        auth=(disco_config["apiKey"], ""),
        headers={"Accept": "application/json"},
        verify=config.requests_verify(disco_config),
    )
    if response.status_code != 201:
        click.echo("Error")
        click.echo(response.text)
        return
    resp_body = response.json()
    click.echo("Project added.")
    if resp_body["project"]["githubRepo"] is not None:
        click.echo("")
        m = re.match(
            r"^((git@)|(https://))github\.com:(?P<repo>\S+)\.git$",
            resp_body["project"]["githubRepo"],
        )
        if m is not None:
            repo = m.group("repo")
        else:
            click.echo(
                f"Couldn't parse Github repo: {resp_body['project']['githubRepo']}"
            )
            repo = "your-repo-here"
    if resp_body["sshKeyPub"] is not None:
        click.echo("")
        click.echo("Github Deploy Key")
        click.echo("=================")
        click.echo("")
        click.echo("You need to give read access to your repo to Disco.")
        click.echo(f"Open https://github.com/{repo}/settings/keys/new")
        click.echo("")
        click.echo('Title: Give it the title you want, for example: "Disco".')
        click.echo("")
        click.echo("Key:")
        click.echo(resp_body["sshKeyPub"])
        click.echo("No need for write access.")
    if resp_body["project"]["githubWebhookToken"] is not None:
        click.echo("")
        webhook_host = resp_body["project"]["domain"]
        if webhook_host is None:
            webhook_host = disco_config["host"]
        click.echo("")
        click.echo("Github Webhook")
        click.echo("==============")
        click.echo("")
        click.echo("To deploy automatically when commits are pushed.")
        click.echo(f"Open https://github.com/{repo}/settings/hooks/new")
        click.echo("")
        click.echo("Payload URL")
        click.echo(
            f"https://{webhook_host}"
            f"/.disco/webhooks/github/{resp_body['project']['githubWebhookToken']}"
        )
        click.echo("")
        click.echo("SSL verification: Enable SSL verification")
        click.echo("Content type: application/json")
        click.echo("Secret: leave empty.")
        click.echo("Just the push event.")
        click.echo('Check "Active".')
    if resp_body["deployment"] is not None:
        project = name
        click.echo(f"Deploying {project}, version {resp_body['deployment']['number']}")
        url = f"https://{disco_config['host']}/.disco/projects/{project}/deployments/{resp_body['deployment']['number']}/output"
        response = requests.get(
            url,
            auth=(disco_config["apiKey"], ""),
            headers={"Accept": "text/event-stream"},
            stream=True,
            verify=config.requests_verify(disco_config),
        )
        for event in sseclient.SSEClient(response).events():
            output = json.loads(event.data)
            click.echo(output["text"], nl=False)
