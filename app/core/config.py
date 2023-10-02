import logging
import os

from dotenv import load_dotenv
from starlette.datastructures import Secret

load_dotenv(override=True)

# General
# ------------------------------------------------------------------------------
DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1")
SECRET_KEY: Secret = Secret(os.getenv("SECRET_KEY", ""))
PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Prem Daemon")
PREMD_IMAGE: str = os.getenv("PREMD_IMAGE", "ghcr.io/premai-io/premd")
DEFAULT_PORT: int = int(os.getenv("DEFAULT_PORT", "8000"))

# PROXY
# ------------------------------------------------------------------------------
PROXY_ENABLED: bool = os.getenv("PROXY_ENABLED", "False").lower() in ("true", "1")
DNSD_URL: str = os.getenv("DNSD_URL", "http://dnsd:8080")

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

# Constants
# ------------------------------------------------------------------------------
DNSD_DNS_EXIST_PATH = "/dns/existing"
DNSD_IP = "/dns/ip"


def dns_exists_url() -> str:
    return f"{DNSD_URL}{DNSD_DNS_EXIST_PATH}"


def dns_ip() -> str:
    return f"{DNSD_URL}{DNSD_IP}"
