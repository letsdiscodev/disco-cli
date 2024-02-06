import click
import requests

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
def projects_add(name: str, domain: str, github_repo: str, disco: str | None) -> None:
    disco_config = config.get_disco(disco)
    click.echo(f"Adding project")
    url = f"https://{disco_config['host']}/.disco/projects"
    req_body = dict(
        name=name,
        githubRepo=github_repo,
        domain=domain,
    )
    response = requests.post(url,
        json=req_body,
        auth=(disco_config["apiKey"], ""),
        headers={"Accept": "application/json"},
        verify=config.requests_verify(disco_config),
    )
    if response.status_code != 201:
        click.echo("Error")
        click.echo(response.text)
    resp_body = response.json()
    if resp_body["sshKeyPub"] is not None:
        click.echo("Create a Deploy Key on Github with this:")
        click.echo(resp_body["sshKeyPub"])
        click.echo("")
    if resp_body["project"]["githubRepo"] is not None:
        webhook_host = resp_body["project"]["domain"]
        if webhook_host is None:
            webhook_host = disco_config['host']
        click.echo(
            "Then add a Github webhook for pushes to that URL, "
            "with 'Content-Type: application/json':"
        )
        click.echo(
            f"https://{webhook_host}"
            f"/.disco/webhooks/github/{resp_body['project']['id']}"
        )
