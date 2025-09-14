from fastapi import APIRouter

from app.api.routes import games, llms, providers, utils, dependencies

api_router = APIRouter()
api_router.include_router(games.router)
api_router.include_router(llms.router)
api_router.include_router(providers.router)
api_router.include_router(utils.router)
api_router.include_router(dependencies.router)