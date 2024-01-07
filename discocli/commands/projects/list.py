import click
import requests

from discocli import config

@click.command(name="projects:list")
@click.option(
    "--disco-domain",
    required=False,
    help="The domain where Disco is running",
)
def projects_list(disco_domain: str | None) -> None:
    disco_domain_config = config.get_disco_domain(disco_domain)
    disco_domain = disco_domain_config["domain"]
    click.echo(f"Listing projects")
    url = f"https://{disco_domain}/projects"
    response = requests.get(url,
        auth=(disco_domain_config["apiKey"], ""),
        headers={"Accept": "application/json"},
    )
    if response.status_code != 200:
        click.echo("Error")
        click.echo(response.text)
        return
    resp_body = response.json()
    for project in resp_body["projects"]:
        click.echo(project["name"])
        click.echo(project["githubRepo"])
        click.echo("")