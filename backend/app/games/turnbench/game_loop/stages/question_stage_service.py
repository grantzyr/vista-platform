from typing import Tuple, Optional, List

from app.core.llm_client import LLMClient
from app.core.exceptions import ResponseFormatError, ResponseNotValidError
from app.core.config import settings
from app.utils import setup_logger
from app.models.llm import LLMCompleteResponse
from app.games.turnbench.verifier.verifier_manager import verifier_manager
from app.games.turnbench.verifier.models import Verifier
from app.games.turnbench.config import GAME_NAME
from app.games.turnbench.models.session import GameSession, PlayTurnData
from app.games.turnbench.game_session.session_service import SessionService
from app.games.turnbench.llm.llm_parser_service import LlmParserService

logger = setup_logger(f"{GAME_NAME}-QuestionStageService", settings.LOG_LEVEL)

class QuestionStageService:
    """question verifier stage service"""
    
    @classmethod
    def execute(
        cls, 
        session: GameSession, 
        session_service: SessionService, 
        llm_client: LLMClient, 
        verifiers: List[Verifier]
    ) -> None:
        """execute question verifier stage"""
        cls.execute_turn(session, session_service, llm_client, verifiers)
    
    @classmethod
    def execute_turn(
        cls, 
        session: GameSession, 
        session_service: SessionService, 
        llm_client: LLMClient, 
        verifiers: List[Verifier], 
        custom_prompt: Optional[str] = None
    ) -> None:
        """execute question verifier stage turn"""
        try:
            step_prompt, reasoning, model_level_reasoning, verifier_choice, verifier_result = cls.handle_question_turn(session, session_service, llm_client, verifiers, custom_prompt)
            logger.debug(f"question stage, verifier_choice: {verifier_choice}, verifier_result: {verifier_result}")
        except Exception as e:
            logger.error(f"question stage, unknown error: {e}")
            session_service.clear_current_turn_data(session)
            raise e

        session_service.update_turn_message_indexes(session)
        session_service.merge_game_messages(session)
        if session_service.check_if_three_questions(session):
            session_service.update_turn_llm_response_indexes(session, len(session.messages)-3)
        else:
            session_service.update_turn_llm_response_indexes(session, len(session.messages)-1)

        session_service.update_game_time(session, session.turn_time_used)
        session_service.merge_game_tokens(session)
        session_service.update_game_turns(session)
    
        session_service.update_turn_result(session,
            PlayTurnData(
                turn_num=session.total_turns,
                round_num=session.total_rounds + 1,
                turn_name="question",
                turn_prompt=step_prompt,
                turn_reasoning=reasoning,
                turn_model_level_reasoning=model_level_reasoning,
                turn_time_used=session.turn_time_used,
                verifier_choice=verifier_choice,
                verifier_result=verifier_result
            )
        )
        session_service.clear_current_turn_data(session)
        session_service.update_next_turn_name(session)
        
    @classmethod
    def handle_question_turn(
        cls, 
        session: GameSession, 
        session_service: SessionService, 
        llm_client: LLMClient, 
        verifiers: List[Verifier], 
        custom_prompt: Optional[str] = None
    ) -> None:
        """handle question turn"""
        step_prompt = custom_prompt if custom_prompt else cls.prepare_prompt_for_round(session, session_service)
        session_service.add_turn_message(session, "user", step_prompt)
        
        reasoning, verifier_choice, llm_response = cls.handle_question(session, session_service, llm_client)
        # get verifier result
        if verifier_choice == "SKIP":
            verifier_result = None
        else:
            guess_code = session_service.get_current_round_guess_code(session)
            if session.mode == "classic":
                verifier_id = session.game_info["verifier_ids"][int(verifier_choice)]
                active_criteria_id = session.game_info["active_criteria_ids"][int(verifier_choice)]
            else:
                verifier_id = session.game_info["nightmare_verifier_ids"][int(verifier_choice)]
                active_criteria_id = session.game_info["nightmare_active_criteria_ids"][int(verifier_choice)]
            verifier = next((v for v in verifiers if v.id == verifier_id), None)
            verifier_result = cls.get_verifier_result(verifier, active_criteria_id, guess_code)
        
        if session_service.check_if_three_questions(session):
            after_last_prompt = session.base_game_prompts["after_last_question_prompt"].format(
                verifier_num=verifier_choice, 
                verifier_result=verifier_result
            )
            session_service.add_turn_message(session, "assistant", after_last_prompt)
            session_service.add_turn_message(session, "assistant", "I will decide whether to proceed to the next round during the Deduce Stage.")
            

        return step_prompt, reasoning, llm_response.model_level_reasoning_content, verifier_choice, verifier_result
        
    @classmethod
    def handle_question(
        cls, 
        session: GameSession, 
        session_service: SessionService, 
        llm_client: LLMClient, 
        format_error_retry_count: int = 0, 
        not_valid_error_retry_count: int = 0
    ) -> Tuple[Optional[str], str, LLMCompleteResponse]:
        """handle question"""
        # get LLM response
        llm_response = llm_client.get_complete(session.messages + session.turn_messages)
        session_service.add_turn_message(session, "assistant", llm_response.content)
        session_service.update_turn_time(session, llm_response.time_used)
        session_service.update_turn_tokens(session, llm_response)
        
        # extract reasoning and verifier choice
        try:
            reasoning, verifier_choice = LlmParserService.extract_verifier_choices(llm_response.content)
            if verifier_choice != "SKIP":
                cls.check_verifier_choice_valid(session, verifier_choice)
        except ResponseFormatError as e:
            if format_error_retry_count > 3:
                raise e
            logger.debug(f"question stage, response format error, retrying, retry_count: {format_error_retry_count}")
            session_service.update_game_response_with_formatting_error(session, 1)
            session_service.add_turn_message(session, "user", session.base_game_prompts["not_valid_question_format_prompt"])
            return cls.handle_question(session, session_service, llm_client, format_error_retry_count + 1, not_valid_error_retry_count)
        except ResponseNotValidError as e:
            if not_valid_error_retry_count > 3:
                raise e
            logger.debug(f"question stage, response not valid error, retrying, retry_count: {not_valid_error_retry_count}")
            session_service.update_game_response_with_not_valid_error(session, 1)
            session_service.add_turn_message(session, "user", session.base_game_prompts["not_valid_verifier_choice_prompt"].format(
                verifier_num=verifier_choice
            ))
            return cls.handle_question(session, session_service, llm_client, format_error_retry_count, not_valid_error_retry_count + 1)
        except Exception as e:
            logger.error(f"question stage, unknown error: {e}")
            raise e
        
        return reasoning, verifier_choice, llm_response
        
    @staticmethod
    def prepare_prompt_for_round(session: GameSession, session_service: SessionService) -> str:
        """prepare current round prompt"""
        question_round = session_service.get_current_question_round(session)
        
        if question_round > 3: # unexpected question round
            raise Exception("Unexpected question round")
        
        if question_round == 1:  # first question
            return session.base_game_prompts["first_question_prompt"].format(
                verifier_descriptions=session.verifier_descriptions
            )
        
        last_question_turn_result = session.turn_result_history[-1]
        
        # following question (2, 3)
        return session.base_game_prompts["following_question_prompt"].format(
            verifier_num=last_question_turn_result["verifier_choice"], 
            verifier_result=last_question_turn_result["verifier_result"]
        )

    @staticmethod
    def get_verifier_result(verifier: Verifier, active_criteria_id: int, guess_code: str) -> str:
        """get verifier result"""
        return "PASS" if verifier_manager.verify(verifier, active_criteria_id, guess_code) else "FAIL"
    
    @staticmethod
    def check_verifier_choice_valid(session: GameSession, verifier_choice: str) -> None:
        """check verifier choice valid"""
        # non-last question verifier choice not valid
        if int(verifier_choice) < 0 or int(verifier_choice) >= len(session.game_info["verifier_ids"]):
            logger.error(f"Verifier choice {verifier_choice} is not valid. Total verifier count: {len(session.game_info["verifier_ids"])}")
            raise ResponseNotValidError(f"Verifier choice {verifier_choice} is not valid.")
    