import os
from typing import List, Dict, Any, Tuple

from app.core.config import settings
from app.utils import setup_logger, load_json, save_json
from .models import Verifier, VerifierPublic
from .criteria_service import CriteriaService

logger = setup_logger("VerifierManager", settings.LOG_LEVEL)

class VerifierManager:
    """Manager for verifier-related operations that implements business logic."""

    def __init__(self):
        self.verifiers = self._load_verifiers()

    def _load_verifiers(self) -> Dict[str, Dict[str, Any]]:
        """load verifiers from json file"""
        filepath = "app/games/turnbench/data/verifiers.json"
        logger.info(f"Trying to load {filepath} to load verifiers")
        verifiers_data = load_json(filepath)
        return verifiers_data

    def get_verifiers(self) -> Dict[str, Dict[str, Any]]:
        """get verifiers"""
        return self.verifiers
    
    def get_verifier_by_id(self, verifier_id: str) -> Verifier:
        """get verifier by id"""
        return Verifier(**self.verifiers.get(str(verifier_id)))
    
    def get_verifier_by_ids(self, verifier_ids: List[int]) -> List[Verifier]:
        """get verifiers by ids"""
        return [self.get_verifier_by_id(str(verifier_id)) for verifier_id in verifier_ids]
    
    def get_verifier_public_by_ids(self, verifier_ids: List[str]) -> List[VerifierPublic]:
        """get verifiers by ids"""
        return [VerifierPublic(**self.verifiers.get(verifier_id)) for verifier_id in verifier_ids]
    
    def create_verifier(self, verifier_info: Verifier) -> bool:
        """create verifier"""
        self.verifiers[verifier_info.id] = verifier_info.model_dump()
        return True
    
    def update_verifier(self, verifier_id: str, verifier_info: Verifier) -> bool:
        """update verifier"""
        self.verifiers[verifier_id] = verifier_info.model_dump()
        return True
    
    def delete_verifiers(self, verifier_ids: List[str]) -> bool:
        """delete verifiers"""
        for verifier_id in verifier_ids:
            self.verifiers.pop(verifier_id)
        return True
    
    def verify(self, verifier_info: Verifier, criterion_id: int, context: str) -> bool:
        """Verify if the criterion is met"""
        criterion = next((c for c in verifier_info.criteria if c.id == criterion_id), None)
        if criterion is None:
            raise ValueError(f"Criterion with id {criterion_id} not found")
        return getattr(CriteriaService, criterion.function)(context)
    
    def get_verifier_descriptions(self, verifier_list: List[Verifier]) -> str:
        """Get all verifier descriptions"""
        if not verifier_list:
            raise ValueError("Verifier list is empty")
        
        descriptions = []
        for i, ver in enumerate(verifier_list):
            desc = f"Verifier <{i}>: {ver.description}"
            # Add criteria description
            criteria_descs = []
            for criterion in ver.criteria:
                criteria_descs.append(f"- Possible criteria: {criterion.description}")
            
            criteria_str = "\n".join(criteria_descs)
            descriptions.append(f"{desc}\n{criteria_str}")
        
        return "\n".join(descriptions)

verifier_manager = VerifierManager()