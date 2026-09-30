"""
Nexa Solutions - AI Software Development Internship
Week 4 - Part D: Script 01 - Model Parameters (Temperature & Max Output Tokens)
File: 01_model_parameters.py
Description: Demonstrates how hyperparameters like 'temperature' and 'max_output_tokens'
             govern LLM output determinism, creativity, and token budget length
             using the Google Gemini API (gemini-1.5-flash).
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Ensure UTF-8 output formatting for Windows console
if sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

def compare_temperature_and_tokens():
    print("=" * 70)
    print("  [Experiment 1] Google Gemini API - Temperature & Token Dynamics")
    print("=" * 70)

    gemini_key = os.getenv("GEMINI_API_KEY")

    prompt = (
        "In exactly three words, describe the primary feeling invoked by "
        "Frank Herbert's sci-fi epic 'Dune'."
    )
    print(f"[*] Prompt: \"{prompt}\"\n")

    if gemini_key and not gemini_key.startswith("your_"):
        try:
            import google.generativeai as genai
            genai.configure(api_key=gemini_key)

            # -----------------------------------------------------------
            # Scenario A: Deterministic Setting (Temperature = 0.0)
            # Low randomness, highly reproducible, factual, strict outputs
            # -----------------------------------------------------------
            print("--- Scenario A: Low Temperature (temperature=0.0, deterministic) ---")
            config_deterministic = genai.types.GenerationConfig(
                temperature=0.0,
                max_output_tokens=50
            )
            model_a = genai.GenerativeModel("gemini-3.8-flash", generation_config=config_deterministic)
            for i in range(2):
                res = model_a.generate_content(prompt)
                print(f"  Run #{i+1}: {res.text.strip()}")

            # -----------------------------------------------------------
            # Scenario B: Creative Setting (Temperature = 1.0)
            # High randomness, wider lexical variation, creative outputs
            # -----------------------------------------------------------
            print("\n--- Scenario B: High Temperature (temperature=1.0, creative) ---")
            config_creative = genai.types.GenerationConfig(
                temperature=1.0,
                max_output_tokens=50
            )
            model_b = genai.GenerativeModel("gemini-3.8-flash", generation_config=config_creative)
            for i in range(2):
                res = model_b.generate_content(prompt)
                print(f"  Run #{i+1}: {res.text.strip()}")

            # -----------------------------------------------------------
            # Scenario C: Token Capping (max_output_tokens = 15)
            # Hard limit capping response generation
            # -----------------------------------------------------------
            print("\n--- Scenario C: Strict Token Cap (max_output_tokens=15) ---")
            long_prompt = "Provide a comprehensive plot overview of the novel 'Dune'."
            config_capped = genai.types.GenerationConfig(
                temperature=0.2,
                max_output_tokens=15
            )
            model_c = genai.GenerativeModel("gemini-3.8-flash", generation_config=config_capped)
            res_capped = model_c.generate_content(long_prompt)
            print(f"  Capped Output: \"{res_capped.text.strip()}\" [Truncated due to token cap]")
            print("\n" + "=" * 70)
            return

        except Exception as ex:
            print(f"[!] Live API note: {ex}. Running educational simulation.\n")

    # Offline Demonstration
    print("--- [Simulation] Low Temperature (temperature=0.0) ---")
    print("  Run #1: Desolate desert power.")
    print("  Run #2: Desolate desert power. (Identical / Deterministic)")

    print("\n--- [Simulation] High Temperature (temperature=1.0) ---")
    print("  Run #1: Vast ecological grandeur.")
    print("  Run #2: Mystical destiny unraveling. (Varied / Creative)")

    print("\n--- [Simulation] Strict Token Cap (max_output_tokens=15) ---")
    print("  Capped Output: 'Dune follows young Paul Atreides as his family moves to the' [Truncated]")
    print("\n" + "=" * 70)

if __name__ == "__main__":
    compare_temperature_and_tokens()
