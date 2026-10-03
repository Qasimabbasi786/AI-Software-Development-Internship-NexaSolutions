"""
Dynamic Multi-Provider Model Factory for Week 6 Part C.

Provides:
- Primary default: Google Gemini via langchain_google_genai (ChatGoogleGenerativeAI)
- Conditional fallbacks: OpenAI (ChatOpenAI), Anthropic (ChatAnthropic)
- Deterministic mock fallback for offline validation
"""
import os
from pathlib import Path
from typing import Optional, Any
from dotenv import load_dotenv

# Load .env locally from module directory first, then root fallback
_part_dir = Path(__file__).resolve().parent
_local_env = _part_dir / ".env"
_root_env = _part_dir.parent / ".env"

if _local_env.exists():
    load_dotenv(dotenv_path=_local_env)
elif _root_env.exists():
    load_dotenv(dotenv_path=_root_env)
else:
    load_dotenv()

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.embeddings import Embeddings
from langchain_core.runnables import RunnableLambda
from langchain_core.messages import AIMessage


def get_chat_model(
    model_name: Optional[str] = None,
    temperature: float = 0.0,
    **kwargs: Any
) -> BaseChatModel:
    """
    Factory function providing the primary Google Gemini model or fallback chat model.
    Prioritizes Google Gemini (`ChatGoogleGenerativeAI`) as the primary driver.
    """
    gemini_key = os.getenv("GEMINI_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")

    # 1. Primary Default: Google Gemini
    if gemini_key:
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            selected_model = model_name or os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
            return ChatGoogleGenerativeAI(
                model=selected_model,
                google_api_key=gemini_key,
                temperature=temperature,
                **kwargs
            )
        except Exception as ex:
            print(f"[ModelFactory] Notice: ChatGoogleGenerativeAI initialization warning: {ex}")

    # 2. Conditional Fallback: OpenAI
    if openai_key:
        try:
            from langchain_openai import ChatOpenAI
            selected_model = model_name or "gpt-4o-mini"
            return ChatOpenAI(
                model=selected_model,
                api_key=openai_key,
                temperature=temperature,
                **kwargs
            )
        except Exception:
            pass

    # 3. Conditional Fallback: Anthropic
    if anthropic_key:
        try:
            from langchain_anthropic import ChatAnthropic
            selected_model = model_name or "claude-3-5-sonnet-20241022"
            return ChatAnthropic(
                model=selected_model,
                api_key=anthropic_key,
                temperature=temperature,
                **kwargs
            )
        except Exception:
            pass

    # 4. Offline Deterministic Mock Runnable Fallback
    def mock_model_invoke(prompt_value):
        text = prompt_value.to_string() if hasattr(prompt_value, "to_string") else str(prompt_value)
        return AIMessage(content="Simulated response for offline execution.")

    return RunnableLambda(mock_model_invoke)
