import os

import sentry_sdk
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import API_PREFIX, DEBUG, PROJECT_NAME
from app.core.events import create_start_app_handler
from app.routes import router as api_router

load_dotenv()


sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    traces_sample_rate=1.0,
)


def get_application() -> FastAPI:
    application = FastAPI(title=PROJECT_NAME, debug=DEBUG, version="0.0.1")
    application.mount(
        "/assets/apps", StaticFiles(directory="./app/assets/"), name="apps"
    )
    application.include_router(api_router, prefix=API_PREFIX)
    application.add_event_handler("startup", create_start_app_handler(application))
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return application


app = get_application()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
