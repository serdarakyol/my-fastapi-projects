from fastapi import APIRouter

from api.routes import router_cf, router_extract_data

api_router = APIRouter()
api_router.include_router(router_cf.router)
api_router.include_router(router_extract_data.router)
