import re
from copy import deepcopy
from typing import Optional, List, Dict, Any, Tuple

import uuid
from fastapi import HTTPException
from sqlmodel import Session

from app.core.config import settings
from app.utils import setup_logger
from app.models.llm import LLM, LLMCompleteResponse
from app.games.turnbench.config import GAME_NAME
from app.games.turnbench.verifier.models import Verifier
from app.games.turnbench.verifier.verifier_manager import verifier_manager
from app.games.turnbench.game_session.session_repository import SessionRepository
from app.games.turnbench.models.session import (
    GameSession, 
    GameSessionCreate, 
    GameSessionUpdate,
    PlayTurnData
)

logger = setup_logger(f"{GAME_NAME}-SessionService", settings.LOG_LEVEL)

class SessionService:
    """
    Service layer for session-related operations.
    """
    def __init__(self, session: Session):
        self.session = session
        self.session_repository = SessionRepository(session)

    def get_sessions(self, page: int, page_size: int, llm_id: Optional[str] = None, setup_id: Optional[str] = None) -> List[GameSession]:
        """get sessions"""
        sessions, total = self.session_repository.list_game_sessions(
            skip=(page - 1) * page_size, 
            limit=page_size, 
            llm_id=llm_id, 
            setup_id=setup_id
        )
        logger.debug(f"get {len(sessions)} sessions")
        return sessions, total

    def get_session_by_id(self, session_id: uuid.UUID) -> GameSession:
        """get session by id"""
        session = self.session_repository.get_game_session_by_id(session_id)
        logger.debug(f"get session by id {session_id}")
        if session is None:
            raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
        return session

    def get_session_by_id_with_llm_info_and_setup_info(self, session_id: uuid.UUID) -> GameSession:
        """get session by id with llm info and setup info"""
        session = self.session_repository.get_game_session_by_id_with_llm_info_and_setup_info(session_id)
        logger.debug(f"get session by id {session_id}")
        if session is None:
            raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
        return session
    
    def create_session(self, session_create: GameSessionCreate) -> GameSession:
        """create session"""
        return self.session_repository.create_game_session(game_session_create=session_create)
    
    def update_session(self, session_id: uuid.UUID, session_update: GameSessionUpdate) -> bool:
        """update session"""
        session = self.session_repository.update_game_session(session_id, session_update)
        logger.debug(f"update session {session_id}")
        return session
    
    def delete_sessions(self, session_id: uuid.UUID) -> Tuple[List[bool], bool]:
        """delete sessions"""
        success = self.session_repository.delete_game_session_by_id(session_id)
        logger.debug(f"delete sessions {session_id}: {success}")
        return success
    
    def copy_session(self, src_session: GameSession, new_llm: Optional[LLM] = None) -> GameSession:
        """Copy a session"""
        new_session = deepcopy(src_session)
        if new_llm:
            new_session.llm_id = new_llm.id
        new_session_create = GameSessionCreate(**new_session.model_dump())
        saved_session = self.create_session(new_session_create)
        return saved_session
    
    def add_message(self, game_session: GameSession | GameSessionCreate, role: str, content: str) -> None:
        """Add message to history"""
        game_session.messages.append({"role": role, "content": content})
    
    def add_turn_message(self, game_session: GameSession, role: str, content: str) -> None:
        """Add turn message to history"""
        game_session.turn_messages.append({"role": role, "content": content})
    
    def merge_game_messages(self, game_session: GameSession) -> None:
        """Merge turn messages"""
        game_session.messages.extend(game_session.turn_messages)

    def add_system_message(self, game_session: GameSession | GameSessionCreate, system_message: Optional[str] = None) -> None:
        """Add system message to history"""
        if system_message is None:
            system_message = game_session.base_game_prompts["system_prompt"].format(
                game_setup=game_session.verifier_descriptions
            )
        self.add_message(game_session, "system", system_message)
    
    def check_total_rounds(self, game_session: GameSession) -> int:
        """Check total rounds"""
        return len([turn["turn_name"] for turn in game_session.turn_result_history if turn["turn_name"] == "deduce"])
    
    def cut_turn_history(self, game_session: GameSession, turn_num: int) -> None:
        """Cut turn history"""
        turn_name = game_session.turn_result_history[turn_num-1]["turn_name"]
        game_session.next_turn_name = turn_name
        game_session.turn_result_history = game_session.turn_result_history[:turn_num-1]
        message_index = game_session.turn_message_indexes[turn_num-1]
        game_session.turn_message_indexes = game_session.turn_message_indexes[:turn_num-1]
        game_session.turn_llm_response_indexes = game_session.turn_llm_response_indexes[:turn_num-1]
        game_session.messages = game_session.messages[:message_index]
        game_session.total_rounds = self.check_total_rounds(game_session)
        game_session.total_turns = turn_num - 1
        game_session.submitted_code = None
        game_session.game_over = False
        game_session.game_over_reason = None
        game_session.game_success = False

    def update_turn_message_indexes(self, game_session: GameSession) -> None:
        """Update turn message indexes"""
        game_session.turn_message_indexes.append(len(game_session.messages))
    
    def update_turn_llm_response_indexes(self, game_session: GameSession, index: int) -> None:
        """Update turn llm response indexes"""
        game_session.turn_llm_response_indexes.append(index)

    def clear_current_turn_data(self, game_session: GameSession) -> None:
        """Clear current turn data"""
        game_session.turn_messages = []
        game_session.turn_time_used = 0
        game_session.turn_input_tokens = 0
        game_session.turn_output_tokens = 0
        game_session.turn_longest_context_length = 0

    def get_current_round_guess_code(self, game_session: GameSession) -> str:
        """Get current round guess code"""
        for turn in game_session.turn_result_history[::-1]:
            if turn["turn_name"] == "proposal":
                return turn["guess_code"]
        return None
    
    def get_current_question_round(self, game_session: GameSession) -> int:
        """Get current question round"""
        return len([turn["turn_name"] for turn in game_session.turn_result_history[-3:] if turn["turn_name"] == "question"]) + 1
    
    def check_if_three_questions(self, game_session: GameSession) -> bool:
        """Check if three questions"""
        return len([turn["turn_name"] for turn in game_session.turn_result_history[-3:] if turn["turn_name"] == "question"]) >= 3
    
    def update_next_turn_name(self, game_session: GameSession) -> None:
        """Update next turn name"""
        if game_session.next_turn_name == "proposal":
            game_session.next_turn_name = "question"
        elif game_session.next_turn_name == "question":
            if game_session.turn_result_history[-1]["turn_name"] == "proposal":
                return
            skip_turn = game_session.turn_result_history[-1]["verifier_choice"] == "SKIP"
            already_three_questions = self.check_if_three_questions(game_session)
            if skip_turn or already_three_questions:
                game_session.next_turn_name = "deduce"
        elif game_session.next_turn_name == "deduce":
            if game_session.game_over:
                game_session.next_turn_name = "end"
            else:
                game_session.next_turn_name = "proposal"
 
    def update_game_tokens(self, game_session: GameSession, llm_response: LLMCompleteResponse) -> None:
        """Update game tokens"""
        game_session.total_input_tokens += llm_response.input_tokens
        game_session.total_output_tokens += llm_response.output_tokens
        game_session.longest_context_length = max(game_session.longest_context_length, llm_response.input_tokens + llm_response.output_tokens)
    
    def update_turn_tokens(self, game_session: GameSession, llm_response: LLMCompleteResponse) -> None:
        """Update turn tokens"""
        game_session.turn_input_tokens += llm_response.input_tokens
        game_session.turn_output_tokens += llm_response.output_tokens
        game_session.turn_longest_context_length = max(game_session.turn_longest_context_length, llm_response.input_tokens + llm_response.output_tokens)
    
    def merge_game_tokens(self, game_session: GameSession) -> None:
        """Merge game tokens"""
        game_session.total_input_tokens += game_session.turn_input_tokens
        game_session.total_output_tokens += game_session.turn_output_tokens
        game_session.longest_context_length = max(game_session.longest_context_length, game_session.turn_longest_context_length)
    
    def update_game_response_with_formatting_error(self, game_session: GameSession, count: int = 1) -> None:
        """Update game response with formatting error"""
        game_session.total_response_with_formatting_error += count
    
    def update_game_time(self, game_session: GameSession, time_used: float) -> None:
        """Update game time"""
        game_session.total_time += time_used
    
    def update_turn_time(self, game_session: GameSession, time_used: float) -> None:
        """Update turn time"""
        game_session.turn_time_used += time_used
    
    def update_game_turns(self, game_session: GameSession, count: int = 1) -> None:
        """Update game turns"""
        game_session.total_turns += count
    
    def update_turn_result(self, game_session: GameSession, result: Optional[PlayTurnData] = None) -> None:
        """Update turn result"""
        if result is None:
            return
        if len(game_session.turn_result_history) >= result.turn_num:
            self.replace_turn_result(game_session, result)
        elif len(game_session.turn_result_history) == result.turn_num - 1:
            game_session.turn_result_history.append(result.model_dump())
        else:
            logger.warning(f"There is a gap in turn results: current reust turn_num: {result.turn_num} - length of history: {len(game_session.turn_result_history)}")
            raise ValueError(f"Turn number {result.turn_num} is out of range")
    
    def replace_turn_result(self, game_session: GameSession, result: PlayTurnData) -> None:
        """Replace turn result"""
        old_turn_result = game_session.turn_result_history[result.turn_num-1]
        turn_name = old_turn_result["turn_name"]
        turn_message_index = game_session.turn_message_indexes[result.turn_num-1]
        turn_llm_response_index = game_session.turn_llm_response_indexes[result.turn_num-1]

        old_prompt = old_turn_result["turn_prompt"]
        new_prompt = result.turn_prompt
        if old_prompt != new_prompt:
            game_session.messages[turn_message_index]["content"] = new_prompt

        old_reasoning = old_turn_result["turn_reasoning"]
        new_reasoning = result.turn_reasoning
        if old_reasoning != new_reasoning:
            game_session.messages[turn_llm_response_index]["content"] = game_session.messages[turn_llm_response_index]["content"].replace(old_reasoning, new_reasoning)

        if turn_name == "proposal":
            old_guess_code = old_turn_result["guess_code"]
            new_guess_code = result.guess_code
            if old_guess_code != new_guess_code:
                choice_tag_match = re.search(r"<CHOICE>", game_session.messages[turn_llm_response_index]["content"], re.IGNORECASE)
                if choice_tag_match:
                    choice_text = game_session.messages[turn_llm_response_index]["content"][choice_tag_match.start():]
                    new_choice_text = f"<CHOICE>: BLUE={new_guess_code[0]} YELLOW={new_guess_code[1]} PURPLE={new_guess_code[2]}"
                    game_session.messages[turn_llm_response_index]["content"] = game_session.messages[turn_llm_response_index]["content"].replace(choice_text, new_choice_text)

        elif turn_name == "question":
            old_verifier_choice = old_turn_result["verifier_choice"]
            new_verifier_choice = result.verifier_choice
            if old_verifier_choice != new_verifier_choice:
                choice_tag_match = re.search(r"<CHOICE>", game_session.messages[turn_llm_response_index]["content"], re.IGNORECASE)
                if choice_tag_match:
                    choice_text = game_session.messages[turn_llm_response_index]["content"][choice_tag_match.start():]
                    new_choice_text = f"<CHOICE>: {new_verifier_choice}"
                    game_session.messages[turn_llm_response_index]["content"] = game_session.messages[turn_llm_response_index]["content"].replace(choice_text, new_choice_text)

            old_verifier_result = old_turn_result["verifier_result"]
            new_verifier_result = result.verifier_result
            if old_verifier_result != new_verifier_result:
                if turn_llm_response_index+1 < len(game_session.messages):
                    game_session.messages[turn_llm_response_index+1]["content"] = game_session.messages[turn_llm_response_index+1]["content"].replace(old_verifier_result, new_verifier_result)


        game_session.turn_result_history[result.turn_num-1] = result.model_dump()

    def update_num_of_verifier_passed(self, game_session: GameSession, submitted_code: str, verifiers: List[Verifier]) -> None:
        """Count the number of verifiers passed"""
        count = 0
        for i, verifier_id in enumerate(game_session.game_info["verifier_ids"]):
            verifier = next((v for v in verifiers if v.id == verifier_id), None)
            criteria_id = game_session.game_info["active_criteria_ids"][i]
            is_passed = verifier_manager.verify(verifier, criteria_id, submitted_code)
            if is_passed:
                count += 1
        game_session.num_of_verifier_passed = count

    def update_submitted_code(self, game_session: GameSession, submitted_code: str) -> None:
        """Update submitted code"""
        game_session.submitted_code = submitted_code

    def update_game_rounds(self, game_session: GameSession, count: int = 1) -> None:
        """Update game rounds"""
        game_session.total_rounds += count

    def update_game_status(self, game_session: GameSession) -> None:
        """Update game status"""
        if game_session.submitted_code:
            game_session.game_over = True
            game_session.game_over_reason = "Submitted"
            game_session.game_success = game_session.submitted_code == game_session.game_info["answer"]
            return
        
        if game_session.total_rounds >= game_session.max_rounds:
            game_session.game_over = True
            game_session.game_over_reason = "Over rounds"
            game_session.game_success = False
            return
        
        game_session.game_over = False
        game_session.game_over_reason = None
        game_session.game_success = False


    def check_answer(self, game_session: GameSession, submitted_code: str) -> bool:
        """Check if the submitted code is correct"""
        return submitted_code == game_session.game_info["answer"]
