from tomllib import load

from src import ROOT_PATH

__all__ = ["get_config"]

CONFIG_PATH = ROOT_PATH / "config.toml"

_config: dict | None = None


def _load_config() -> None:
    global _config

    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"{CONFIG_PATH} not found")

    with open(CONFIG_PATH, "rb") as file:
        _config = load(file)


def get_config(section: str) -> dict:
    if _config is None:
        _load_config()

    if not section in _config:
        raise KeyError(f"{section} not found in config")

    return _config[section]
