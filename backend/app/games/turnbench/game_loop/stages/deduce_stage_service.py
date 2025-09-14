from typing import Tuple, Optional, List

from app.core.llm_client import LLMClient
from app.core.exceptions import ResponseFormatError
from app.core.config import settings
from app.utils import setup_logger
from app.models.llm import LLMCompleteResponse
from app.games.turnbench.verifier.models import Verifier
from app.games.turnbench.config import GAME_NAME
from app.games.turnbench.models.session import GameSession, PlayTurnData
from app.games.turnbench.game_session.session_service import SessionService
from app.games.turnbench.llm.llm_parser_service import LlmParserService

logger = setup_logger(f"{GAME_NAME}-DeduceStageService", settings.LOG_LEVEL)

class DeduceStageService:
    """deduce stage service"""
    
    @classmethod
    def execute(
        cls, 
        session: GameSession, 
        session_service: SessionService, 
        llm_client: LLMClient, 
        verifiers: List[Verifier]
    ) -> None:
        """execute deduce stage"""
        cls.execute_turn(session, session_service, llm_client, verifiers)
    
    @classmethod
    def execute_turn(
        cls, 
        session: GameSession, 
        session_service: SessionService, 
        llm_client: LLMClient, 
        verifiers: List[Verifier], 
        custom_prompt: Optional[str] = None) -> None:
        """execute deduce turn"""
        try:
            step_prompt = custom_prompt if custom_prompt else session.base_game_prompts["deduce_prompt"]
            session_service.add_turn_message(session, "user", step_prompt)
            
            reasoning, submitted_code, llm_response = cls.handle_deduce(session, session_service, llm_client)
            
            if submitted_code:
                guess_correct = session_service.check_answer(session, submitted_code)
                session_service.update_submitted_code(session, submitted_code)
                session_service.update_num_of_verifier_passed(session, submitted_code, verifiers)

                result_prompt = session.base_game_prompts["deduce_result_prompt"].format(
                    submitted_code=submitted_code, 
                    answer=session.game_info["answer"], 
                    is_correct=guess_correct
                )
                session_service.add_turn_message(session, "user", result_prompt)

            logger.debug((
                f"deduce stage completed, submitted: {'Not submitted' if not submitted_code else submitted_code}, "
                f"guess_correct: {'Not submitted' if not submitted_code else 'Correct' if guess_correct else 'Incorrect'}, "
            ))
        except Exception as e:
            logger.error(f"deduce stage, unknown error: {e}")
            raise e
        
        session_service.update_turn_message_indexes(session)
        session_service.merge_game_messages(session)
        if submitted_code:
            session_service.update_turn_llm_response_indexes(session, len(session.messages)-2)
        else:
            session_service.update_turn_llm_response_indexes(session, len(session.messages)-1)
            
        session_service.update_game_time(session, session.turn_time_used)
        session_service.merge_game_tokens(session)
        session_service.update_game_turns(session)
        session_service.update_game_rounds(session)
        session_service.update_game_status(session)

        session_service.update_turn_result(session,
            PlayTurnData(
                turn_num=session.total_turns,
                round_num=session.total_rounds,
                turn_name="deduce",
                turn_prompt=step_prompt,
                turn_reasoning=reasoning,
                turn_model_level_reasoning=llm_response.model_level_reasoning_content,
                turn_time_used=session.turn_time_used,
                deduce_choice_skip=submitted_code is None,
                deduce_choice_submit_code=submitted_code,
                is_game_over=session.game_over,
                game_over_reason=session.game_over_reason,
                game_success=session.game_success
            )
        )
        session_service.clear_current_turn_data(session)
        session_service.update_next_turn_name(session)

    @classmethod  
    def handle_deduce(
        cls, 
        session: GameSession, 
        session_service: SessionService, 
        llm_client: LLMClient, 
        retry_count: int = 0
    ) -> Tuple[Optional[str], Optional[str], LLMCompleteResponse]:
        """handle deduce"""
        llm_response = llm_client.get_complete(session.messages + session.turn_messages)
        session_service.add_turn_message(session, "assistant", llm_response.content)
        session_service.update_turn_time(session, llm_response.time_used)
        session_service.update_turn_tokens(session, llm_response)
        
        try:
            reasoning, submitted_code = LlmParserService.extract_deduce(llm_response.content)
        except ResponseFormatError as e:
            if retry_count > 3:
                raise e
            session_service.update_game_response_with_formatting_error(session, 1)
            logger.debug(f"deduce stage, response format error, retrying, retry_count: {retry_count}")
            session_service.add_turn_message(session, "user", session.base_game_prompts["not_valid_deduce_format_prompt"])
            return cls.handle_deduce(session, session_service, llm_client, retry_count + 1)
        except Exception as e:
            logger.debug(f"deduce stage, unknown error: {e}")
            raise e
        
        return reasoning, None if submitted_code == "SKIP" else submitted_code, llm_response
