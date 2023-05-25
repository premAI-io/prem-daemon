import logging

from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

# General
# ------------------------------------------------------------------------------
DEBUG: bool = config("DEBUG", cast=bool, default=False)
SECRET_KEY: Secret = config("SECRET_KEY", cast=Secret, default="")
PROJECT_NAME: str = config("PROJECT_NAME", default="Prem Box")

# APIs
# ------------------------------------------------------------------------------
API_PREFIX = "/api/v1"
API_VERSION = "0.1.0"

# Prem Registry
# ------------------------------------------------------------------------------
PREM_REGISTRY_URL: str = config(
    "PREM_REGISTRY_URL", default="https://prem-registry.fly.dev"
)

# Logging
# ------------------------------------------------------------------------------
logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
