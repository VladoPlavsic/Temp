from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every

from starlette.requests import Request
from starlette.responses import Response

from app.api.routes import router as api_router
from app.core import config, tasks
from app.api.dependencies.email import send_message
import requests
import logging

logger = logging.getLogger(__name__)

def setup_logger():
    logging.basicConfig(
        filename=config.LOG_FILE,
        format='%(asctime)s [%(levelname)-8s] %(message)s',
        level=config.LOG_LEVEL,
        datefmt='%Y-%m-%d %H:%M:%S')

def get_application():
    setup_logger()

    app = FastAPI(title=config.PROJECT_NAME, version=config.VERSION)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[config.SITE_URL],
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PUT"],
        allow_headers=["Content-Type","Set-Cookie"],
    )

    # Send email on server error
    async def catch_exceptions_middleware(request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            send_message(subject="Server error", message_text=f"Error on server occured. {e}")
            logger.error("----- 500 INTERNAL SERVER ERROR -----")
            logger.exception(e)
            logger.error("----- 500 INTERNAL SERVER ERROR -----")
            return Response("Internal server error", status_code=500)

    # Add middleware for sending error email
    app.middleware('http')(catch_exceptions_middleware)

    app.add_event_handler("startup", tasks.create_start_app_handler(app))
    app.add_event_handler("shutdown", tasks.create_stop_app_handler(app))

    # weekly sharing link update
    @app.on_event("startup")
    @repeat_every(seconds=6 * 24 * 60 * 60) # update every 6 days
    def update_cdn_sharing_links() -> None:
        logger.warn(f"sending PUT request to {config.RESFUL_SERVER_URL}/api/public/update/")
        requests.put(f"{config.RESFUL_SERVER_URL}/api/private/update/")

    # Keep server alive
    # @app.on_event("startup")
    # @repeat_every(seconds=60 * 25) # update every 25 minutes (Keep server alive, remove on paid version)
    # def keep_server_alive() -> None:
    #     logger.warn(f"sending GET request to {config.RESFUL_SERVER_URL}/api/public/wake/")
    #     requests.get(f"{config.RESFUL_SERVER_URL}/api/public/wake/")

    app.include_router(api_router, prefix="/api")

    return app

app = get_application()
