from typing import List

from pydantic import BaseModel

class CriteriaBase(BaseModel):
    id: int
    description: str

class VerifierBase(BaseModel):
    id: int
    description: str

class VerifierPublic(VerifierBase):
    criteria: List[CriteriaBase]

class Criteria(CriteriaBase):
    function: str

class Verifier(VerifierBase):
    criteria: List[Criteria]
    created_at: str
    updated_at: str