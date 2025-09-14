import uuid
from fastapi import APIRouter, HTTPException

from app.api.deps import SessionDep
from app.core.config import settings
from app.utils import setup_logger
from app.services import LLMService
from app.models.llm import LLMCreate, LLMUpdate, LLMPublic, LLMListResponse, LLMInfoResponse, LLMDeleteResponse

router = APIRouter(prefix="/llms", tags=["llms"])
logger = setup_logger("llms-router", settings.LOG_LEVEL)
            
@router.get("", response_model=LLMListResponse)
def get_llms(page: int, page_size: int, db_session: SessionDep):
    try:
        llm_service = LLMService(db_session)
        llms, total = llm_service.get_llms_public_page(page=page, page_size=page_size)
        logger.info(f"get {total} llms")
        return LLMListResponse(data=llms, count=total, page=page, page_size=page_size)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting llms: {e}")

@router.get("/{llm_id}", response_model=LLMInfoResponse)
def get_llm(llm_id: uuid.UUID, db_session: SessionDep):
    try:
        llm_service = LLMService(db_session)
        llm_public = llm_service.get_llm_public_by_llm_id(llm_id)
        if not llm_public:
            raise HTTPException(status_code=404, detail=f"LLM with id {llm_id} not found")
        return LLMInfoResponse(data=llm_public)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting llm: {e}")

@router.post("", response_model=LLMPublic)
def create_llm(
    llm_request: LLMCreate,
    db_session: SessionDep
):
    try:
        llm_service = LLMService(db_session)
        llm = llm_service.create_llm(llm_request)
        return LLMPublic(**llm.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating llm: {e}")

@router.put("/{llm_id}", response_model=LLMPublic)
def update_llm(
    llm_id: uuid.UUID,
    llm_request: LLMUpdate,
    db_session: SessionDep
):
    try:
        llm_service = LLMService(db_session)
        llm = llm_service.update_llm(llm_id, llm_request)
        return LLMPublic(**llm.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating llm: {e}")

@router.delete("/{llm_id}", response_model=LLMDeleteResponse)
def delete_llm(
    llm_id: uuid.UUID,
    db_session: SessionDep
):
    try:
        llm_service = LLMService(db_session)
        deleted = llm_service.delete_llm(llm_id)
        if not deleted:
            raise HTTPException(status_code=404, detail=f"LLM with id {llm_id} not deleted")
        return LLMDeleteResponse(data=llm_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting llm: {e}")