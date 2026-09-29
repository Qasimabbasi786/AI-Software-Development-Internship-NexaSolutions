"""
Week 3 - Part G: AI & Python Foundations (Kickoff)
File: main.py
Description: Python AI foundation script demonstrating LLM API communication, 
             environment key isolation, prompt variations, and hallucination handling.
"""

import os
import sys
from dotenv import load_dotenv
import anthropic

# 1. Load environment variables from local .env file
load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key or api_key == "your_anthropic_api_key_here":
    print("[!] Warning: ANTHROPIC_API_KEY is not configured in local .env file.")
    print("    Please set a valid key inside .env before running LLM API requests.")
    sys.exit(1)

# 2. Initialize Anthropic Client
client = anthropic.Anthropic(api_key=api_key)

def run_prompt_experiment(prompt_text: str, description: str, system_prompt: str = None):
    """
    Executes a prompt call against the Claude LLM model and prints the output.
    """
    print(f"\n==================================================")
    print(f" EXPERIMENT: {description}")
    print(f"==================================================")
    if system_prompt:
        print(f"System Role Prompt: {system_prompt}")
    print(f"User Prompt: {prompt_text}")
    print("--------------------------------------------------")

    try:
        kwargs = {
            "model": "claude-sonnet-4-6",
            "max_tokens": 300,
            "messages": [{"role": "user", "content": prompt_text}]
        }
        if system_prompt:
            kwargs["system"] = system_prompt

        response = client.messages.create(**kwargs)
        output_text = response.content[0].text
        print(f"LLM Response:\n{output_text}\n")
    except Exception as ex:
        print(f"API Call Error: {ex}\n")

def main():
    print("--------------------------------------------------")
    print(" Week 3 Part G: AI & LLM Foundation Script")
    print("--------------------------------------------------")

    # 1. Standard Prompt: Definition of Token
    run_prompt_experiment(
        prompt_text="Explain what a token is in the context of LLMs in one concise paragraph.",
        description="Standard Query (Token Definition)"
    )

    # 2. Prompt Variation: Plain Question vs Direct Instruction vs Persona Prompt
    run_prompt_experiment(
        prompt_text="Who was Faiz Ahmed Faiz and what is his legacy in Islamabad's literary culture?",
        description="Prompt Variation 1: Plain Question"
    )

    run_prompt_experiment(
        prompt_text="Summarize the core themes of Faiz Ahmed Faiz's poetry in exactly 3 bullet points.",
        description="Prompt Variation 2: Direct Instruction"
    )

    run_prompt_experiment(
        prompt_text="What books are available in the library?",
        description="Prompt Variation 3: Strict Persona Role",
        system_prompt="You are a strict librarian who only answers in exactly one sentence and speaks formally."
    )

    # 3. Hallucination Test: Made-up / Obscure Entity Query
    run_prompt_experiment(
        prompt_text="Provide a detailed summary of the 1994 Islamabad Cybernetic Quantum Computer Conference organized by Professor Tariq Hashmi.",
        description="Experiment 2: Hallucination Test (Fictional Event)"
    )

if __name__ == "__main__":
    main()
