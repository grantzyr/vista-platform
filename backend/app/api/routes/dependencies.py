import json

import uuid
from fastapi import APIRouter, HTTPException

from app.api.deps import SessionDep
from app.core.config import settings
from app.core.llm_client import LLMClient
from app.utils import setup_logger
from app.services import LLMService
from app.models.dependency import ParseDependencyRequest, ParseDependencyResponse, DependencyItem

router = APIRouter(prefix="/dependencies", tags=["dependencies"])
logger = setup_logger("dependencies-router", settings.LOG_LEVEL)

PARSE_DEPENDENCY_PROMPT = """**Reasoning History:**
{reasoning_history}


Based on the provided Reasoning History, please identify and analyze the dependencies between different turns. 
Your goal is to construct a complete inference path diagram that shows how each turn is supported by one or more previous turns.

Please provide your response as a JSON array, with each object representing a turn and its dependencies. The required format is as follows:
```
{{
    "answer": [
        {{
            "current_turn": turn_num,
            "dependency_turns": [turn_num1, ...],
            "reason": "Provide a concise explanation for why this turn's reasoning is based on the specific dependency turns mentioned."
        }},
        ...
    ]
}}
```
"""

@router.post("", response_model=ParseDependencyResponse)
def parse_dependencies(
    parse_dependency_request: ParseDependencyRequest,
    db_session: SessionDep
):
    try:
        llm_service = LLMService(db_session)
        llm_info = llm_service.get_llm_with_provider_info(parse_dependency_request.llm_id)
        llm_public = llm_service.get_llm_public_by_llm_id(parse_dependency_request.llm_id)

        reasoning_history_str = json.dumps(parse_dependency_request.model_dump()["reasoning_history"])

        llm_client = LLMClient(llm_public, llm_info.provider, json_format=True)
        llm_completion = llm_client.get_complete(
            messages=[
                {
                    "role": "user",
                    "content": PARSE_DEPENDENCY_PROMPT.format(reasoning_history=reasoning_history_str)
                }
            ]
        )
        json_content = json.loads(llm_completion.content)
        if isinstance(json_content, dict) and "answer" in json_content and isinstance(json_content["answer"], list):
            return ParseDependencyResponse(data=json_content["answer"])
        else:
            logger.error(f"parse dependencies: invalid response format: {llm_completion.content}")
            raise KeyError("Invalid response format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parse dependencies: {e}")