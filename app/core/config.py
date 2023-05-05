import logging

from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

# General APIs settings
# ------------------------------------------------------------------------------
API_PREFIX = "/api"
API_VERSION = "0.1.0"

# General Project settings
# ------------------------------------------------------------------------------
DEBUG: bool = config("DEBUG", cast=bool, default=False)
SECRET_KEY: Secret = config("SECRET_KEY", cast=Secret, default="")
PROJECT_NAME: str = config("PROJECT_NAME", default="ai_box")

# Logging settings
# ------------------------------------------------------------------------------
logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Model settings
# ------------------------------------------------------------------------------
MODEL_ID: str = config("MODEL_ID", default="gpt4all-j-v1.3-groovy")
MODEL_WEIGHTS_DIR: str = config("MODEL_WEIGHTS_DIR", default="./models")
