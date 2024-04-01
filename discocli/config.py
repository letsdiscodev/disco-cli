import os
from typing import Any, Literal
import json
from pathlib import Path


HOME_DIR = Path.home()
CONFIG_PATH = f"{HOME_DIR}/.disco/config.json"
CONFIG_FOLDER = f"{HOME_DIR}/.disco"
CERTS_FOLDER = f"{HOME_DIR}/.disco/certs"

# TODO dataclass for disco config


def add_disco(
    name: str,
    host: str,
    ip: str,
    api_key: str,
    public_key: str | None = None,
) -> None:
    config = _get_config()
    if name in config["discos"]:
        raise Exception(f"Disco {name} already in config")
    config["discos"][name] = {
        "name": name,
        "host": host,
        "ip": ip,
        "apiKey": api_key,
    }
    _save_config(config)
    if public_key is not None:
        _write_cert(ip, public_key)


def disco_already_in_config(name: str) -> bool:
    config = _get_config()
    return name in list(config["discos"].keys())

def get_disco(name: str | None) -> dict[str, Any]:
    config = _get_config()
    if name is None:
        discos = list(config["discos"].keys())
        if len(discos) != 1:
            raise Exception("Please specify --disco")
        name = discos[0]
    return config["discos"][name]


def get_api_key(disco: str | None = None) -> str:
    disco_config = get_disco(disco)
    return disco_config["apiKey"]


def set_host(name: str, host: str) -> dict[str, Any]:
    config = _get_config()
    if name == config["discos"][name]["host"]:
        config["discos"][host] = config["discos"][name]
        config["discos"][host]["name"] = host
        del config["discos"][name]
        name = host
    config["discos"][name]["host"] = host
    _save_config(config)
    return get_disco(name)


def _get_config():
    if not os.path.exists(CONFIG_PATH):
        # default
        return dict(discos=dict())
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_config(config: dict[str, Any]) -> None:
    if not os.path.isdir(CONFIG_FOLDER):
        os.makedirs(CONFIG_FOLDER)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)


def _cert_path(ip: str) -> str:
    return f"{CERTS_FOLDER}/{ip}.crt"


def _write_cert(ip: str, public_key: str) -> None:
    if not os.path.isdir(CONFIG_FOLDER):
        os.makedirs(CONFIG_FOLDER)
    if not os.path.isdir(CERTS_FOLDER):
        os.makedirs(CERTS_FOLDER)
    with open(_cert_path(ip), "w", encoding="utf-8") as f:
        f.write(public_key)


def requests_verify(disco_config: dict[str, Any]) -> Literal[True] | str:
    """Returns the value for the param 'verify' in requests.

    True means "verify the TLS certificate provided by the server.
    The path to the certificate means "verify the certificate
    provided by the server using the public key.

    We're using a self-signed certificate when accessing the
    disco using the IP address instead of a domain name.

    """
    if disco_config["host"] != disco_config["ip"]:
        # sending request to domain name
        return True
    return _cert_path(disco_config["ip"])
