import uuid
from fastapi import APIRouter, HTTPException

from app.api.deps import SessionDep
from app.core.config import settings
from app.utils import setup_logger
from app.services import GameHistoryService
from app.models.history import (
    GameHistoryListResponse, 
    GameHistoryPublic,
    GameHistoryUpdate,
    GameHistoryDeleteResponse,
)

router = APIRouter(prefix="/history", tags=["history"])
logger = setup_logger("history-router", settings.LOG_LEVEL)
            
@router.get("", response_model=GameHistoryListResponse)
def get_games(page: int, page_size: int, db_session: SessionDep):
    try:
        history_service = GameHistoryService(db_session)
        histories, total = history_service.get_game_histories_public_page(page=page, page_size=page_size)
        logger.info(f"get {total} histories")
        return GameHistoryListResponse(data=histories, count=total, page=page, page_size=page_size)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting histories: {e}")
    
@router.get("/{session_id}", response_model=GameHistoryPublic)
def get_game_by_id(session_id: uuid.UUID, db_session: SessionDep):
    try:
        history_service = GameHistoryService(db_session)
        history = history_service.get_game_history_public_by_id(session_id)
        logger.info(f"get history {session_id} success")
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting history {session_id}: {e}")

@router.put("/{session_id}", response_model=GameHistoryPublic)
def update_history(
    session_id: uuid.UUID,
    history_request: GameHistoryUpdate,
    db_session: SessionDep
):
    try:
        history_service = GameHistoryService(db_session)
        history = history_service.update_game_history(session_id, history_request)
        return GameHistoryPublic(**history.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating llm: {e}")

@router.delete("/{session_id}", response_model=GameHistoryDeleteResponse)
def delete_history(session_id: uuid.UUID, db_session: SessionDep):
    try:
        history_service = GameHistoryService(db_session)
        deleted = history_service.delete_game_history(session_id)
        if not deleted:
            raise HTTPException(status_code=404, detail=f"History with id {session_id} not deleted")
        return GameHistoryDeleteResponse(data=session_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting llm: {e}")