"""
Week 7 Security Layer: Input & Output Guardrails
Implements:
1. Input Guard: detects blatant prompt injections, system prompt override attempts, and instruction breakouts.
2. Output Guard: scans model responses before delivery to redact or block leaked API keys, JWT tokens, connection strings, or internal prompt templates.
"""

import re
from typing import Tuple, Optional

# Regex patterns for secret detection
JWT_PATTERN = re.compile(r"eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{4,}")
API_KEY_PATTERN = re.compile(r"(AIza[0-9A-Za-z-_]{35}|sk-[a-zA-Z0-9]{32,}|AQ\.[a-zA-Z0-9_-]{40,})")
CONN_STR_PATTERN = re.compile(r"(Host=[^;\n]+|Server=[^;\n]+|Password=[^;\n]+)", re.IGNORECASE)

# Dangerous directive patterns in user input
OVERRIDE_PATTERNS = [
    re.compile(r"ignore\s+(all\s+)?(previous\s+)?(instructions|rules|prompts)", re.IGNORECASE),
    re.compile(r"print\s+(your\s+)?(system\s+)?prompt", re.IGNORECASE),
    re.compile(r"(output|show|reveal)\s+(your\s+)?(api\s+keys?|secret|credentials)", re.IGNORECASE),
    re.compile(r"you\s+are\s+now\s+in\s+developer\s+mode", re.IGNORECASE),
    re.compile(r"system:\s*reserve", re.IGNORECASE),
]

class SecurityGuardrails:

    @staticmethod
    def validate_input(user_prompt: str) -> Tuple[bool, Optional[str]]:
        """Scans incoming user input for direct prompt injection attempts.
        Returns: (is_safe, failure_reason)"""
        for pattern in OVERRIDE_PATTERNS:
            if pattern.search(user_prompt):
                return False, "Input flagged by security guardrail: Direct instruction override attempt detected."
        return True, None

    @staticmethod
    def sanitize_output(response_text: str) -> str:
        """Sanitizes model output, redacting any accidentally exposed secrets or authorization tokens."""
        # 1. Redact JWT tokens
        sanitized = JWT_PATTERN.sub("[REDACTED_JWT_TOKEN]", response_text)
        # 2. Redact API keys
        sanitized = API_KEY_PATTERN.sub("[REDACTED_API_KEY]", sanitized)
        # 3. Redact Database connection parameters
        sanitized = CONN_STR_PATTERN.sub("[REDACTED_CREDENTIALS]", sanitized)
        return sanitized
