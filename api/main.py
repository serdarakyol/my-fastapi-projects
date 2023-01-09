from fastapi import FastAPI

from api.core.config import API_PREFIX, APP_NAME, APP_VERSION, IS_DEBUG
from api.core.event_handler import start_app_handler, stop_app_handler
from api.routes.router_cf import router_cf
from api.routes.router_xlsx import router_xlsx

def get_app() -> FastAPI:
    fast_app = FastAPI(title=APP_NAME, version=APP_VERSION, debug=IS_DEBUG)
    fast_app.include_router(router_cf, prefix=API_PREFIX)
    fast_app.include_router(router_xlsx, prefix=API_PREFIX)

    fast_app.add_event_handler("startup", start_app_handler(fast_app))
    fast_app.add_event_handler("shutdown", stop_app_handler(fast_app))

    return fast_app


app = get_app()
