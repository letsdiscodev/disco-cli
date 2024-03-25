import click
import requests
import sseclient
import json

from discocli import config


@click.command(name="projects:move")
@click.option(
    "--project",
    required=True,
    help="the project name",
)
@click.option(
    "--from-disco",
    required=True,
    help="The Disco to export the project from",
)
@click.option(
    "--to-disco",
    required=True,
    help="The Disco to import the project to",
)
def projects_move(project: str, from_disco: str, to_disco) -> None:
    # export
    from_disco_config = config.get_disco(from_disco)
    to_disco_config = config.get_disco(to_disco)
    url = f"https://{from_disco_config['host']}/.disco/projects/{project}/export"
    response = requests.get(
        url,
        auth=(from_disco_config["apiKey"], ""),
        headers={"Accept": "application/json"},
        verify=config.requests_verify(from_disco_config),
    )
    if response.status_code != 200:
        click.echo("Error")
        click.echo(response.text)
        return
    resp_body = response.json()
    # create project
    url = f"https://{to_disco_config['host']}/.disco/projects"
    req_body = {
        "name": resp_body["name"],
        "githubRepo": resp_body["githubRepo"],
        "domain": resp_body["domain"],
        "githubWebhookToken": resp_body["githubWebhookToken"],
        "ssh": resp_body["ssh"],
        "envVariables": resp_body["envVariables"],
        "caddy": resp_body["caddy"],
        "commit": resp_body["deployment"]["commit"],
        "deploymentNumber": resp_body["deployment"]["number"] + 1,
        "deploy": True,
    }
    response = requests.post(
        url,
        json=req_body,
        auth=(to_disco_config["apiKey"], ""),
        headers={"Accept": "application/json"},
        verify=config.requests_verify(to_disco_config),
    )
    if response.status_code != 201:
        click.echo("Error")
        click.echo(response.text)
        return
    resp_body = response.json()
    if resp_body["deployment"] is not None:
        click.echo(f"Deploying {project}, version {resp_body['deployment']['number']}")
        url = f"https://{to_disco_config['host']}/.disco/projects/{project}/deployments/{resp_body['deployment']['number']}/output"
        response = requests.get(
            url,
            auth=(to_disco_config["apiKey"], ""),
            headers={"Accept": "text/event-stream"},
            stream=True,
            verify=config.requests_verify(to_disco_config),
        )
        for event in sseclient.SSEClient(response).events():
            output = json.loads(event.data)
            click.echo(output["text"], nl=False)
