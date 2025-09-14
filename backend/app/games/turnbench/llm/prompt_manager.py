import os
from typing import List, Dict, Any, Tuple

from app.core.config import settings
from app.utils import setup_logger, load_json
from ..models.llm import Prompt

logger = setup_logger("PromptService", settings.LOG_LEVEL)

class PromptManager:
    """manager for prompt-related operations that implements business logic."""

    def __init__(self):
        self.prompts = self._load_prompts()
    
    def _load_prompts(self) -> Dict[str, str]:
        """load prompts from json file"""
        filepath = "app/games/turnbench/data/prompts.json"
        logger.info(f"Trying to load {filepath} to load prompts")
        return load_json(filepath)
    
    def get_prompts(self) -> Dict[str, str]:
        """get prompts"""
        return self.prompts
    
    def get_prompt_by_name(self, prompt_name: str) -> str:
        """get prompt by name"""
        return self.prompts.get(prompt_name, "")
    
    def update_prompt(self, prompt_name: str, prompt_content: str) -> bool:
        """update prompt"""
        self.prompts[prompt_name] = prompt_content
        return True
    
    def delete_prompts(self, prompt_names: List[str]) -> bool:
        """delete prompts"""
        for prompt_name in prompt_names:
            self.prompts.pop(prompt_name, None)
        return True
    
    def build_prompt_model(self, mode: str) -> Prompt:
        """Build the prompt model"""
        prompts = {}
        # get prompt categories
        for prompt_category in Prompt.model_fields:
            if prompt_category == "system_prompt":
                current_prompt_name = f"{mode}_{prompt_category}"
            else:
                current_prompt_name = f"{mode}_{prompt_category}_with_reasoning_with_hint"
            prompts[prompt_category] = self.prompts.get(current_prompt_name, "")
        return Prompt(**prompts)

prompt_manager = PromptManager()