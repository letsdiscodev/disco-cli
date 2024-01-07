import os
from typing import Any
import json
from pathlib import Path


HOME_DIR = Path.home()
CONFIG_PATH = f"{HOME_DIR}/.disco/config.json"
CONFIG_FOLDER = f"{HOME_DIR}/.disco"

def set_api_key(disco_domain: str, api_key: str) -> None:
    config = _get_config()
    if disco_domain not in config:
        config["discoDomains"][disco_domain] = dict(
            domain=disco_domain,
        )
    config["discoDomains"][disco_domain]["apiKey"] = api_key
    _save_config(config)


def get_disco_domain(disco_domain: str | None) -> dict[str, Any]:
    config = _get_config()
    if disco_domain is None:
        disco_domains = list(config["discoDomains"].keys())
        if len(disco_domains) != 1:
            raise Exception("Please specify --disco-domain")
        disco_domain = disco_domains[0]
    return config["discoDomains"][disco_domain]

def get_api_key(disco_domain: str | None=None) -> str:
    disco_domain_config = get_disco_domain(disco_domain)
    return disco_domain_config["apiKey"]


def _get_config():
    if not os.path.exists(CONFIG_PATH):
        # default
        return dict(discoDomains=dict())
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_config(config: dict[str, Any]) -> None:
    if not os.path.isdir(CONFIG_FOLDER):
        os.makedirs(CONFIG_FOLDER)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)
