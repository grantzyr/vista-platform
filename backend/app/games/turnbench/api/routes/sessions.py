import uuid
from typing import Optional
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException

from app.core.config import settings
from app.core.llm_client import LLMClient
from app.utils import setup_logger
from app.api.deps import SessionDep
from app.models.llm import LLMPublic
from app.services.llm_service import LLMService
from app.games.turnbench.config import GAME_NAME
from app.games.turnbench.game_loop.game_loop_service import GameLoopService
from app.games.turnbench.game_session.session_service import SessionService
from app.games.turnbench.game_setup.setup_service import SetupService
from app.games.turnbench.llm.prompt_manager import prompt_manager
from app.games.turnbench.verifier.verifier_manager import verifier_manager
from app.games.turnbench.models.session import (
    GameSessionPublic,
    GameSessionCreate,
    GameSessionUpdate,
    GetSessionsResponse,
    GetSessionResponse,
    GetSessionTurnHistoryResponse,
    CreateSessionRequest, 
    CreateSessionResponse,
    UpdateSessionRequest,
    UpdateSessionResponse,
    CopySessionRequest,
    CopySessionResponse,
    PlayTurnRequest,
    PlayTurnResponse,
    PlayTurnData,
    SaveSessionRequest,
    SaveSessionResponse,
    ReloadSessionResponse
)
from app.games.turnbench.models.setup import GameSetupDetail

router = APIRouter(prefix=f"/{GAME_NAME}/sessions", tags=[f"{GAME_NAME}-sessions"])
logger = setup_logger(f"{GAME_NAME}-sessions-router", settings.LOG_LEVEL)

@router.get("", response_model=GetSessionsResponse)
def get_sessions(
    db_session: SessionDep,
    page: int,
    page_size: int,
    llm_id: Optional[uuid.UUID] = None,
    setup_id: Optional[uuid.UUID] = None
):
    try:
        session_service = SessionService(db_session)
        sessions, total = session_service.get_sessions(page, page_size, llm_id, setup_id)
        logger.info(f"get {len(sessions)} sessions")
        return GetSessionsResponse(
            data=[GameSessionPublic(**session.model_dump()) for session in sessions],
            count=total,
            page=page,
            page_size=page_size
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting sessions: {e}")

@router.get("/{session_id}", response_model=GetSessionResponse)
def get_specific_session(
    session_id: uuid.UUID,
    db_session: SessionDep
):
    try:
        session_service = SessionService(db_session)
        session = session_service.get_session_by_id(session_id)
        logger.info(f"get session {session_id} success")
        return GetSessionResponse(data=GameSessionPublic(**session.model_dump()))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting session: {e}")

@router.get("/{session_id}/history/turn", response_model=GetSessionTurnHistoryResponse)
def get_session_turn_history(
    session_id: uuid.UUID,
    db_session: SessionDep
):
    try:
        session_service = SessionService(db_session)
        session = session_service.get_session_by_id(session_id)
        logger.info(f"get session {session_id} turn history success")
        return GetSessionTurnHistoryResponse(data=session.turn_result_history)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting session turn history: {e}")

@router.post("", response_model=CreateSessionResponse)
def create_session(
    session_request: CreateSessionRequest,
    db_session: SessionDep
):
    try:
        session_service = SessionService(db_session)
        setup_service = SetupService(db_session)
        setup_info = setup_service.get_setup_public_by_setup_id(session_request.setup_id)
        
        verifier_details = verifier_manager.get_verifier_by_ids(setup_info.verifier_ids)
        verifier_descriptions = verifier_manager.get_verifier_descriptions(verifier_details)

        game_info_detail = GameSetupDetail(
            **setup_info.model_dump(), 
            verifier_details=[vd.model_dump() for vd in verifier_details]
        )

        game_info_detail_json = game_info_detail.model_dump()
        game_info_detail_json["id"] = str(game_info_detail.id)
        game_info_detail_json["created_at"] = game_info_detail.created_at.isoformat()
        game_info_detail_json["updated_at"] = game_info_detail.updated_at.isoformat()

        base_prompts = prompt_manager.build_prompt_model(mode=session_request.mode)

        session_create = GameSessionCreate(
            **session_request.model_dump(),
            game_info=game_info_detail_json,
            verifier_descriptions=verifier_descriptions,
            base_game_prompts=base_prompts.model_dump()
        )
        session_service.add_system_message(session_create)

        game_session = session_service.create_session(session_create)
        
        logger.info(f"create session {game_session.id} success")
        return CreateSessionResponse(data=GameSessionPublic(**game_session.model_dump()))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating session: {e}")

@router.put("/{session_id}", response_model=UpdateSessionResponse)
def update_session(
    session_id: uuid.UUID,
    update_request: UpdateSessionRequest,
    db_session: SessionDep
):
    try:
        session_service = SessionService(db_session)
        session = session_service.get_session_by_id(session_id)
        if update_request.new_turn_data:
            session_service.update_turn_result(session, update_request.new_turn_data)
        session_service.update_session(
            session_id, 
            GameSessionUpdate(
                **session.model_dump(), 
            )
        )
        return UpdateSessionResponse(data=session.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating session: {e}")

@router.post("/{session_id}/copy", response_model=CopySessionResponse)
def copy_session(
    session_id: uuid.UUID,
    copy_request: CopySessionRequest,
    db_session: SessionDep
):
    try:
        session_service = SessionService(db_session)
        source_session = session_service.get_session_by_id(session_id)
        new_llm = None
        if copy_request.new_llm_id:
            new_llm = LLMService(db_session).get_llm_by_id(copy_request.new_llm_id)
        new_session = session_service.copy_session(source_session, new_llm)
        if copy_request.new_turn_data:
            session_service.update_turn_result(new_session, copy_request.new_turn_data)
            session_service.update_session(new_session.id, GameSessionUpdate(**new_session.model_dump()))

        logger.info(f"copy session {new_session.id} from {session_id} success")
        return CopySessionResponse(data=new_session.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error copying session: {e}")

@router.post("/{session_id}/play/turn", response_model=PlayTurnResponse)
def play_turn(
    session_id: uuid.UUID,
    play_request: PlayTurnRequest,
    db_session: SessionDep
):
    try:
        session_service = SessionService(db_session)
        session_info = session_service.get_session_by_id_with_llm_info_and_setup_info(session_id)
        llm_info = LLMPublic(**session_info.llm.model_dump())
        provider_info = session_info.llm.provider
        llm_client = LLMClient(llm_info, provider_info, play_request.reasoning_effort)
        verifiers = verifier_manager.get_verifier_by_ids(session_info.game_info["verifier_ids"])

        GameLoopService.run_turn(session_info, session_service, llm_client, verifiers, play_request.turn_num)
        session_saved = session_service.update_session(session_id, GameSessionUpdate(**session_info.model_dump()))
        logger.info(f"play turn for session {session_id} success")
        return PlayTurnResponse(data=PlayTurnData(**session_saved.turn_result_history[-1]))
    except Exception as e:
        logger.error(f"Error playing turn for session {session_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error playing turn: {e}")