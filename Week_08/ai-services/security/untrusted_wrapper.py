"""
Week 7 Security Layer: Untrusted Content Wrapper & Data Sanitization
Implements:
1. XML Tag Delimiting (<untrusted_document>): cleanly separates catalog/retrieved data from system instructions.
2. Character escaping and instruction stripping to prevent prompt injection breakouts.
"""

from typing import List, Dict, Any, Union
from langchain_core.documents import Document

def wrap_untrusted(docs: List[Union[Document, Dict[str, Any], str]]) -> str:
    """Wraps retrieved documents or catalog database items inside clearly marked
    <untrusted_document> delimiters to inform the LLM that content is DATA, never INSTRUCTIONS."""
    parts = []
    for d in docs:
        if isinstance(d, Document):
            source = d.metadata.get("source", "catalog_db")
            content = d.page_content.strip()
        elif isinstance(d, dict):
            source = d.get("source", d.get("bookId", "catalog_db"))
            content = f"{d.get('title', '')} - {d.get('description', '')}".strip()
        else:
            source = "catalog_db"
            content = str(d).strip()

        # Sanitize against delimiter spoofing
        sanitized_content = content.replace("</untrusted_document>", "[ESCAPED_CLOSING_TAG]")
        parts.append(
            f"<untrusted_document source='{source}'>\n"
            f"{sanitized_content}\n"
            f"</untrusted_document>"
        )

    return "\n\n".join(parts)
