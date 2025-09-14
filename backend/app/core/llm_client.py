import time
from typing import Dict, List, Any, Optional

from openai import OpenAI
from openai.types.chat import ChatCompletion

from app.models.provider import Provider
from app.models.llm import LLMPublic, LLMCompleteResponse

class LLMClient:
    """Base LLM client class, handling shared logic for all providers"""

    def __init__(
        self, 
        model_info: LLMPublic, 
        provider_info: Provider, 
        reasoning_effort: Optional[str] = None, 
        json_format: Optional[bool] = None,
    ) -> None:
        """initialize the base client"""
        self.model_info = model_info
        self.provider_info = provider_info
        self.reasoning_effort = reasoning_effort
        self.json_format = json_format
        client_kwargs = {"api_key": provider_info.api_key}
        if provider_info.base_url:
            client_kwargs["base_url"] = provider_info.base_url
        self.client = OpenAI(**client_kwargs)

    def _get_structured_response(self, response: ChatCompletion, time_used: float, model: Optional[LLMPublic] = None) -> LLMCompleteResponse:
        """Get structured response from OpenAI API"""
        model_outputs = LLMCompleteResponse(**{
            "provider_id": self.provider_info.id,
            "provider_name": self.provider_info.display_name,
            "llm_id": model.id if model else self.model_info.id,
            "llm_name": model.name if model else self.model_info.name,
            "time_used": time_used,
            "content": response.choices[0].message.content.strip(),
            "model_level_reasoning_content": getattr(response.choices[0].message, 'reasoning_content', None),
            "input_tokens": response.usage.prompt_tokens,
            "output_tokens": response.usage.completion_tokens,
        })
        return model_outputs

    def get_complete(self, messages: List[Dict[str, Any]], model: Optional[LLMPublic] = None, **kwargs) -> LLMCompleteResponse:
        """use the API to generate a completion"""
        try:
            params = {
                "model": model.name if model else self.model_info.name, 
                "messages": messages,
                **kwargs
            }
            if self.reasoning_effort:
                params["reasoning_effort"] = self.reasoning_effort
            if self.json_format:
                params["response_format"] = {"type": "json_object"}

            start_time = time.time()
            response = self.client.chat.completions.create(**params)
            end_time = time.time()
            time_used = end_time - start_time
            if response.choices:
                return self._get_structured_response(response, time_used, model)
            else:
                raise KeyError("No response choices found.")
        except Exception as e:
            raise e