import logging
import os

from dotenv import load_dotenv
from starlette.datastructures import Secret

load_dotenv(override=True)

# General
# ------------------------------------------------------------------------------
DEBUG: bool = os.getenv("DEBUG", False)
SECRET_KEY: Secret = Secret(os.getenv("SECRET_KEY", ""))
PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Prem Daemon")
 
# APIs
# ------------------------------------------------------------------------------
API_PREFIX = "/v1"
API_VERSION = "0.1.0"

# Prem Registry
# ------------------------------------------------------------------------------
PREM_REGISTRY_URL: str = os.getenv(
    "PREM_REGISTRY_URL",
    "https://raw.githubusercontent.com/premAI-io/prem-registry/main/manifests.json",
)

# Logging
# ------------------------------------------------------------------------------
logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
