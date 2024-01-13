import click
import requests

from discocli import config

@click.command(name="projects:add")
@click.option(
    "--name",
    required=True,
    help="the name that you'll use to refer to the project",
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
    "--disco-domain",
    required=False,
    help="The domain where Disco is running",
)
def projects_add(name: str, domain: str, github_repo: str, disco_domain: str | None) -> None:
    disco_domain_config = config.get_disco_domain(disco_domain)
    disco_domain = disco_domain_config["domain"]
    click.echo(f"Adding project")
    url = f"https://{disco_domain}/projects"
    req_body = dict(
        name=name,
        githubRepo=github_repo,
        domain=domain,
    )
    response = requests.post(url,
        json=req_body,
        auth=(disco_domain_config["apiKey"], ""),
        headers={"Accept": "application/json"},
    )
    if response.status_code != 201:
        click.echo("Error")
        click.echo(response.text)
    resp_body = response.json()
    click.echo("Create a Deploy Key on Github with this:")
    click.echo(resp_body["sshKeyPub"])
    click.echo("")
    click.echo("Then add a Github webhook for pushes to that URL, "
               "with 'Content-Type: application/json':")
    click.echo(f"https://{disco_domain}/webhooks/github/{resp_body['project']['id']}")
