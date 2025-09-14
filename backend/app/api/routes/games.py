import uuid
from fastapi import APIRouter, HTTPException

from app.api.deps import SessionDep
from app.core.config import settings
from app.utils import setup_logger
from app.services import GameService
from app.models.game import GameListResponse, GamePublic, GameDeleteResponse

router = APIRouter(prefix="/games", tags=["games"])
logger = setup_logger("games-router", settings.LOG_LEVEL)
            
@router.get("", response_model=GameListResponse)
def get_games(page: int, page_size: int, session: SessionDep):
    try:
        game_service = GameService(session)
        games, total = game_service.get_games_public_page(page=page, page_size=page_size)
        logger.info(f"get {total} games")
        return GameListResponse(data=games, count=total, page=page, page_size=page_size)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting setups: {e}")
    
@router.get("/{game_id}", response_model=GamePublic)
def get_game_by_id(game_id: uuid.UUID, session: SessionDep):
    try:
        game_service = GameService(session)
        game = game_service.get_game_public_by_id(game_id)
        logger.info(f"get game {game_id} success")
        return game
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting game {game_id}: {e}")