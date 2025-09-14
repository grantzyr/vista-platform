from typing import Tuple, Optional

from app.core.llm_client import LLMClient
from app.core.exceptions import ResponseFormatError
from app.core.config import settings
from app.utils import setup_logger
from app.models.llm import LLMCompleteResponse
from app.games.turnbench.config import GAME_NAME
from app.games.turnbench.models.session import GameSession, PlayTurnData
from app.games.turnbench.game_session.session_service import SessionService
from app.games.turnbench.llm.llm_parser_service import LlmParserService

logger = setup_logger(f"{GAME_NAME}-ProposalStageService", settings.LOG_LEVEL)

class ProposalStageService:
    """proposal stage service"""

    @classmethod
    def execute(cls, session: GameSession, session_service: SessionService, llm_client: LLMClient) -> None:
        """execute proposal stage"""
        cls.execute_turn(session, session_service, llm_client)

    @classmethod
    def execute_turn(cls, session: GameSession, session_service: SessionService, llm_client: LLMClient, custom_prompt: Optional[str] = None) -> None:
        """execute proposal stage turn"""
        try:
            step_prompt = custom_prompt if custom_prompt else session.base_game_prompts["proposal_prompt"]
            session_service.add_turn_message(session, "user", step_prompt)
            
            reasoning, guess_code, llm_response = cls.handle_proposal(session, session_service, llm_client)

            logger.debug(f"proposal stage, guess_code: {guess_code}")
        except Exception as e:
            logger.error(f"proposal stage, unknown error: {e}")
            session_service.clear_current_turn_data(session)
            raise e
        
        session_service.update_turn_message_indexes(session)
        session_service.merge_game_messages(session)
        session_service.update_turn_llm_response_indexes(session, len(session.messages)-1)
        session_service.update_game_time(session, session.turn_time_used)
        session_service.merge_game_tokens(session)
        session_service.update_game_turns(session)

        # SessionService.update_all_guesses(session, guess_code)
        session_service.update_turn_result(session,
            PlayTurnData(
                turn_num=session.total_turns,
                round_num=session.total_rounds + 1,
                turn_name="proposal",
                turn_prompt=step_prompt,
                turn_reasoning=reasoning,
                turn_model_level_reasoning=llm_response.model_level_reasoning_content,
                turn_time_used=session.turn_time_used,
                guess_code=guess_code
            )
        )
        session_service.clear_current_turn_data(session)
        session_service.update_next_turn_name(session)
        logger.debug(f"proposal stage completed, next turn: {session.next_turn_name}")
        
    @classmethod
    def handle_proposal(
        cls, 
        session: GameSession, 
        session_service: SessionService, 
        llm_client: LLMClient, 
        retry_count=0
    ) -> Tuple[Optional[str], Optional[str], Optional[LLMCompleteResponse]]:
        """handle proposal"""
        llm_response = llm_client.get_complete(session.messages + session.turn_messages)
        session_service.add_turn_message(session, "assistant", llm_response.content)
        session_service.update_turn_time(session, llm_response.time_used)
        session_service.update_turn_tokens(session, llm_response)
        
        try:
            reasoning, guess_code = LlmParserService.extract_proposal(llm_response.content)
            return reasoning, guess_code, llm_response
        except ResponseFormatError as e:
            session_service.update_game_response_with_formatting_error(session, 1)
            if retry_count > 3:
                logger.error(f"proposal stage, response format error, retry_count: {retry_count} exceeded max retry count")
                raise e
            logger.debug(f"proposal stage, response format error, retrying, retry_count: {retry_count}")
            session_service.add_turn_message(session, "user", session.base_game_prompts["not_valid_proposal_format_prompt"])
            return cls.handle_proposal(session, session_service, llm_client, retry_count + 1)
        except Exception as e:
            logger.error(f"proposal stage, unknown error: {e}")
            raise e