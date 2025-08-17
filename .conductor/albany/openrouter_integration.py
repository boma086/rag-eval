import os
from typing import Any, Dict, List, Optional
from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_core.outputs import ChatResult, ChatGeneration
import openai
from config import EVALUATOR_CONFIG

class ChatOpenRouter(BaseChatModel):
    """OpenRouter chat model integration for LangChain.
    
    This class provides a wrapper for using OpenRouter API with LangChain,
    allowing access to various language models including OpenAI, Gemini, Claude, etc.
    """
    
    openrouter_api_key: str = None
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    model: str = "gpt-3.5-turbo"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Use the API key from config if not provided
        if not self.openrouter_api_key and EVALUATOR_CONFIG.get("api_key"):
            self.openrouter_api_key = EVALUATOR_CONFIG["api_key"]
        if EVALUATOR_CONFIG.get("base_url"):
            self.openrouter_base_url = EVALUATOR_CONFIG["base_url"]
        if EVALUATOR_CONFIG.get("model"):
            self.model = EVALUATOR_CONFIG["model"]
    
    @property
    def _llm_type(self) -> str:
        return "openrouter"
    
    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        # Convert LangChain messages to OpenAI format
        openai_messages = []
        for message in messages:
            if isinstance(message, SystemMessage):
                openai_messages.append({"role": "system", "content": message.content})
            elif isinstance(message, HumanMessage):
                openai_messages.append({"role": "user", "content": message.content})
            elif isinstance(message, AIMessage):
                openai_messages.append({"role": "assistant", "content": message.content})
        
        # Initialize OpenAI client with OpenRouter configuration
        client = openai.OpenAI(
            api_key=self.openrouter_api_key,
            base_url=self.openrouter_base_url
        )
        
        # Make API call to OpenRouter
        response = client.chat.completions.create(
            model=self.model,
            messages=openai_messages,
            **kwargs
        )
        
        # Convert response to LangChain format
        ai_message = AIMessage(content=response.choices[0].message.content)
        generation = ChatGeneration(message=ai_message)
        return ChatResult(generations=[generation])