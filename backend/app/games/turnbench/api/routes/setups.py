from fastapi import APIRouter, Depends, HTTPException

from app.core.config import settings
from app.utils import setup_logger
from app.api.deps import SessionDep
from app.games.turnbench.config import GAME_NAME, GAME_DISPLAY_NAME, GAME_DESCRIPTION
from app.games.turnbench.models.setup import GameSetupListResponse, GameSetupDetailResponse, GameSetupDetail
from app.games.turnbench.game_setup.setup_service import SetupService
from app.games.turnbench.verifier.verifier_manager import verifier_manager

router = APIRouter(prefix=f"/{GAME_NAME}/setups", tags=[f"{GAME_NAME}-setups"])
logger = setup_logger(f"{GAME_NAME}-setups-router", settings.LOG_LEVEL)
            
@router.get("", response_model=GameSetupListResponse)
def get_setups(page: int, page_size: int, db_session: SessionDep):
    try:
        setup_service = SetupService(db_session)
        setups, total = setup_service.list_setups(page, page_size)
        logger.info(f"get {total} setups")
        return GameSetupListResponse(data=setups, count=total, page=page, page_size=page_size)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting setups: {e}")
    
@router.get("/{setup_id}", response_model=GameSetupDetailResponse)
def get_setup_detail_by_id(
    setup_id: str, 
    db_session: SessionDep
):
    try:
        setup_service = SetupService(db_session)
        setup = setup_service.get_setup_public_by_setup_id(setup_id)
        verifier_details = verifier_manager.get_verifier_by_ids(setup.verifier_ids)
        logger.info(f"get setup detail for {setup_id} success")
        return GameSetupDetailResponse(data=GameSetupDetail(**setup.model_dump(), verifier_details=[vd.model_dump() for vd in verifier_details]))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting setup detail: {e}")