import re
import time
from typing import List, Dict, Any, Optional

from app.core.config import settings
from app.utils import setup_logger
from app.core.llm_client import LLMClient
from app.games.turnbench.config import GAME_NAME
from app.games.turnbench.verifier.models import Verifier
from app.games.turnbench.models.session import GameSession
from app.games.turnbench.game_session.session_service import SessionService
from app.games.turnbench.game_loop.stages import (
    ProposalStageService, 
    QuestionStageService, 
    DeduceStageService
)

logger = setup_logger(f"{GAME_NAME}-GameLoopService", settings.LOG_LEVEL)

class GameLoopService:
    """
    Main game loop service, controlling the entire game process
    """
    @classmethod
    def run_turn(
        cls, 
        session: GameSession, 
        session_service: SessionService,
        llm_client: LLMClient, 
        verifiers: List[Verifier], 
        specific_turn_num: Optional[int] = None
    ) -> None:
        custom_prompt = None
        if specific_turn_num is not None:
            custom_prompt = session.turn_result_history[specific_turn_num-1]["turn_prompt"]
            session_service.cut_turn_history(session, specific_turn_num)
        cls.execute_turn(session, session_service, llm_client, verifiers, custom_prompt)

    @staticmethod
    def execute_turn(
        session: GameSession, 
        session_service: SessionService,
        llm_client: LLMClient, 
        verifiers: List[Verifier],
        custom_prompt: Optional[str] = None
    ) -> None:
        if session.next_turn_name == "proposal":
            logger.debug(f"{session.id}: proposal stage started")
            ProposalStageService.execute_turn(session, session_service, llm_client, custom_prompt)
        elif session.next_turn_name == "question":
            logger.debug(f"{session.id}: question stage started")
            QuestionStageService.execute_turn(session, session_service, llm_client, verifiers, custom_prompt)
        elif session.next_turn_name == "deduce":
            logger.debug(f"{session.id}: deduce stage started")
            DeduceStageService.execute_turn(session, session_service, llm_client, verifiers, custom_prompt)
        elif session.next_turn_name == "end":
            logger.debug(f"{session.id}: Game Ended")
        else:
            raise ValueError(f"Invalid turn name: {session.next_turn_name}")