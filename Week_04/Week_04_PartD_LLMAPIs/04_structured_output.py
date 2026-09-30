"""
Nexa Solutions - AI Software Development Internship
Week 4 - Part D: Script 04 - Structured JSON Outputs & Defensive Parsing
File: 04_structured_output.py
Description: Demonstrates prompting LLMs for structured JSON adhering to a specific
             schema, paired with defensive, resilient try/except parsing using json.loads
             and regex fallbacks.
"""

import os
import sys
import json
import re
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Ensure UTF-8 output formatting for Windows console
if sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

def parse_llm_json_safely(raw_output: str) -> Optional[Dict[str, Any]]:
    """
    Robust JSON parser:
    1. Removes markdown code block delimiters (```json ... ```)
    2. Strips surrounding conversational filler
    3. Traps json.JSONDecodeError with regex bracket extraction
    """
    cleaned = raw_output.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    elif cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    cleaned = cleaned.strip()

    # Step 1: Direct JSON parsing
    try:
        data = json.loads(cleaned)
        if isinstance(data, dict):
            return data
    except json.JSONDecodeError:
        pass

    # Step 2: Regular Expression fallback for embedded JSON object
    match = re.search(r'(\{[\s\S]*\})', raw_output)
    if match:
        try:
            data = json.loads(match.group(1))
            if isinstance(data, dict):
                return data
        except json.JSONDecodeError:
            pass

    return None

def demonstrate_structured_json():
    print("=" * 70)
    print("  [Experiment 4] Google Gemini API - Structured JSON & Defensive Parsing")
    print("=" * 70)

    gemini_key = os.getenv("GEMINI_API_KEY")
    book_title = "Design Patterns: Elements of Reusable Object-Oriented Software"
    book_description = "Gang of Four classic cataloging 23 creational, structural, and behavioral patterns for OOP."

    prompt = f"""Return ONLY valid JSON, no surrounding commentary, adhering strictly to this schema:
{{
  "title": "{book_title}",
  "genre": "primary genre string",
  "key_takeaways": ["takeaway 1", "takeaway 2", "takeaway 3"],
  "summary": "one concise paragraph string"
}}

Book Description: {book_description}
"""

    print(f"[*] Prompting model for structured schema on '{book_title}'...\n")

    raw_response = None

    if gemini_key and not gemini_key.startswith("your_"):
        try:
            import google.generativeai as genai
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel("gemini-3.8-flash")
            response = model.generate_content(prompt)
            raw_response = response.text
        except Exception as ex:
            print(f"[!] Live API note: {ex}. Running simulated parser verification.\n")

    if not raw_response:
        # Realistic raw output containing markdown codeblocks and conversational wrap
        raw_response = f"""Certainly! Here is your requested JSON object:
```json
{{
  "title": "{book_title}",
  "genre": "Software Architecture & Object-Oriented Design",
  "key_takeaways": [
    "Favor object composition over class inheritance",
    "Program to an interface, not an implementation",
    "Encapsulate the concept that varies"
  ],
  "summary": "Design Patterns provides timeless architectural blueprints for structuring flexible, maintainable, and reusable object-oriented codebases."
}}
```
Hope this is helpful!"""

    print("[*] Raw LLM Output Received:")
    print("-" * 50)
    print(raw_response)
    print("-" * 50)

    # Parse and validate with defensive error handling
    parsed_json = parse_llm_json_safely(raw_response)

    if parsed_json:
        print("\n[+] SUCCESS: Defensively Parsed & Validated JSON Dictionary:")
        print(f"    - Title:       {parsed_json.get('title')}")
        print(f"    - Genre:       {parsed_json.get('genre')}")
        print(f"    - Takeaways:   {len(parsed_json.get('key_takeaways', []))} points extracted")
        print(f"    - Summary:     {parsed_json.get('summary')}")
    else:
        print("\n[-] FAILED: Response could not be parsed into a JSON dictionary.")

    print("=" * 70)

if __name__ == "__main__":
    demonstrate_structured_json()
