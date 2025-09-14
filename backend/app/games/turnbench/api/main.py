from fastapi import APIRouter

from app.games.turnbench.api.routes import sessions, setups

turnbench_api_router = APIRouter()
turnbench_api_router.include_router(sessions.router)
turnbench_api_router.include_router(setups.router)