"""
Week 4 - Part D: Structured JSON Output Parsing with Resilient Error Handling
"""

import json
import re
from typing import Optional, Dict, Any

def parse_llm_json_response(raw_output: str) -> Optional[Dict[str, Any]]:
    """
    Robust JSON parser that strips markdown fences, handles stray text,
    and catches JSONDecodeError gracefully.
    """
    # 1. Strip markdown code block wrappers if present
    cleaned = raw_output.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    elif cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    cleaned = cleaned.strip()

    # 2. Attempt parsing JSON directly
    try:
        data = json.loads(cleaned)
        return data
    except json.JSONDecodeError:
        pass

    # 3. Fallback regex extraction if model included conversational prefix/suffix
    match = re.search(r'(\{.*\})', raw_output, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    return None

def test_structured_output():
    print("=== Structured JSON Extraction Test ===")
    sample_raw_llm = """
Here is the JSON you requested:
```json
{
  "title": "Design Patterns",
  "genre": "Software Architecture",
  "summary": "Elements of Reusable Object-Oriented Software describes 23 classic design patterns."
}
```
Hope this helps!
"""
    result = parse_llm_json_response(sample_raw_llm)
    print(f"Extracted Result: {json.dumps(result, indent=2)}")
    if result and "genre" in result:
        print(f"Successfully retrieved genre: {result['genre']}")

if __name__ == "__main__":
    test_structured_output()
