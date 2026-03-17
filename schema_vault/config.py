import os
import sys
from pathlib import Path

try:
    import tomllib
except ImportError:
    import tomli as tomllib  # type: ignore


CONFIG_FILE = "schema-vault.toml"

DEFAULTS = {
    "driver": "sqlite",
    "connection": "./dev.db",
    "migrations_dir": "./migrations",
    "lock_table": "_schema_vault",
}


def load_config(path: str | None = None) -> dict:
    config_path = Path(path or CONFIG_FILE)

    if not config_path.exists():
        # Fall back to environment variables
        return {
            "driver":          os.getenv("SV_DRIVER",         DEFAULTS["driver"]),
            "connection":      os.getenv("SV_CONNECTION",     DEFAULTS["connection"]),
            "migrations_dir":  os.getenv("SV_MIGRATIONS_DIR", DEFAULTS["migrations_dir"]),
            "lock_table":      os.getenv("SV_LOCK_TABLE",     DEFAULTS["lock_table"]),
        }

    with open(config_path, "rb") as f:
        data = tomllib.load(f)

    return {**DEFAULTS, **data}


def write_default_config(name: str = "."):
    target = Path(name) / CONFIG_FILE
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        f"""# Schema Vault configuration
driver = "postgres"
connection = "postgresql://user:password@localhost:5432/{Path(name).name}"
migrations_dir = "./migrations"
lock_table = "_schema_vault"
"""
    )
    return target
