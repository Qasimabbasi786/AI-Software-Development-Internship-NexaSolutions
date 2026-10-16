"""
Dynamic Multi-Provider Model Factory for Week 6 Final Project AI Service.

Provides:
- Primary default: Google Gemini via langchain_google_genai (ChatGoogleGenerativeAI & GoogleGenerativeAIEmbeddings)
- Conditional fallbacks: OpenAI (ChatOpenAI / OpenAIEmbeddings), Anthropic (ChatAnthropic)
- Deterministic mock fallback for offline validation
"""
import os
from pathlib import Path
from typing import Optional, Any
from dotenv import load_dotenv

_current_dir = Path(__file__).resolve().parent
_local_env = _current_dir / ".env"
_root_env = _current_dir.parent.parent / ".env"

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
        if "generate" in text.lower() and "perspectives" in text.lower():
            lines = [
                "Alternative view on books and tech",
                "Related concepts in software architecture and sci-fi",
                "Catalog search query regarding topic"
            ]
            return AIMessage(content="\n".join(lines))
        return AIMessage(content="Catalog information based on verified documents.")

    return RunnableLambda(mock_model_invoke)


def get_embeddings(
    model_name: Optional[str] = None,
    **kwargs: Any
) -> Embeddings:
    """
    Factory function providing embeddings with Google Gemini as primary default.
    """
    gemini_key = os.getenv("GEMINI_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    # 1. Primary Default: Google Gemini Embeddings
    if gemini_key:
        try:
            from langchain_google_genai import GoogleGenerativeAIEmbeddings
            selected_model = model_name or os.getenv("GEMINI_EMBEDDING_MODEL", "models/gemini-embedding-001")
            return GoogleGenerativeAIEmbeddings(
                model=selected_model,
                google_api_key=gemini_key,
                **kwargs
            )
        except Exception as ex:
            print(f"[ModelFactory] Notice: GoogleGenerativeAIEmbeddings warning: {ex}")

    # 2. Conditional Fallback: OpenAI
    if openai_key:
        try:
            from langchain_openai import OpenAIEmbeddings
            selected_model = model_name or "text-embedding-3-small"
            return OpenAIEmbeddings(
                model=selected_model,
                api_key=openai_key,
                **kwargs
            )
        except Exception:
            pass

    # 3. Deterministic Mock Embeddings Fallback
    class MockEmbeddings(Embeddings):
        def embed_documents(self, texts: list[str]) -> list[list[float]]:
            return [[0.05] * 768 for _ in texts]

        def embed_query(self, text: str) -> list[float]:
            return [0.05] * 768

    return MockEmbeddings()
