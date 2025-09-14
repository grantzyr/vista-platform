from typing import Optional

from pydantic import BaseModel

class Prompt(BaseModel):
    system_prompt: str
    proposal_prompt: str
    not_valid_proposal_format_prompt: str
    first_question_prompt: str
    following_question_prompt: str
    after_last_question_prompt: str
    not_valid_verifier_choice_prompt: str
    not_valid_question_format_prompt: str
    deduce_prompt: str
    not_valid_deduce_format_prompt: str
    deduce_result_prompt: str 
