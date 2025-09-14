import uuid
from fastapi import APIRouter, HTTPException

from app.api.deps import SessionDep
from app.core.config import settings
from app.utils import setup_logger
from app.services.provider_service import ProviderService
from app.models.provider import ProviderCreate, ProviderUpdate, ProviderPublic, ProviderListResponse, ProviderDeleteResponse

router = APIRouter(prefix="/providers", tags=["providers"])
logger = setup_logger("providers-router", settings.LOG_LEVEL)
            
@router.get("", response_model=ProviderListResponse)
def get_providers(page: int, page_size: int, db_session: SessionDep):
    try:
        provider_service = ProviderService(db_session)
        providers, total = provider_service.get_providers_public_page(page=page, page_size=page_size)
        logger.info(f"get {total} providers")
        return ProviderListResponse(data=providers, count=total, page=page, page_size=page_size)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting providers: {e}")

@router.post("", response_model=ProviderPublic)
def create_provider(
    provider_request: ProviderCreate,
    db_session: SessionDep
):
    try:
        provider_service = ProviderService(db_session)
        provider = provider_service.create_provider(provider_request)
        return ProviderPublic(**provider.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating provider: {e}")

@router.get("/{provider_id}", response_model=ProviderPublic)
def get_provider(
    provider_id: uuid.UUID,
    db_session: SessionDep
):
    try:
        provider_service = ProviderService(db_session)
        return provider_service.get_provider_public_by_id(provider_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting provider: {e}")

@router.put("/{provider_id}", response_model=ProviderPublic)
def update_provider(
    provider_id: uuid.UUID,
    provider_request: ProviderUpdate,
    db_session: SessionDep
):
    try:
        provider_service = ProviderService(db_session)
        provider = provider_service.update_provider(provider_id, provider_request)
        return ProviderPublic(**provider.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating provider: {e}")

@router.delete("/{provider_id}", response_model=ProviderDeleteResponse)
def delete_provider(
    provider_id: uuid.UUID,
    db_session: SessionDep
):
    try:
        provider_service = ProviderService(db_session)
        deleted = provider_service.delete_provider(provider_id)
        if not deleted:
            raise HTTPException(status_code=404, detail=f"Provider with id {provider_id} not deleted")
        return ProviderDeleteResponse(data=provider_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting provider: {e}")
