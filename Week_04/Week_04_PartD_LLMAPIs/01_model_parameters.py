"""
Nexa Solutions - AI Software Development Internship
Week 4 - Part D: Script 01 - Model Parameters (Temperature & Max Output Tokens)
File: 01_model_parameters.py
Description: Demonstrates how hyperparameters like 'temperature' and 'max_output_tokens'
             govern LLM output determinism, creativity, and token budget length
             using the official modern Google GenAI SDK (google-genai) and gemini-3.8-flash.
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
    print("  [Experiment 1] Google GenAI SDK - Temperature & Token Dynamics")
    print("=" * 70)

    gemini_key = os.getenv("GEMINI_API_KEY")

    prompt = (
        "In exactly three words, describe the primary feeling invoked by "
        "Frank Herbert's sci-fi epic 'Dune'."
    )
    print(f"[*] Prompt: \"{prompt}\"\n")

    if gemini_key and not gemini_key.startswith("your_"):
        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=gemini_key)

            # -----------------------------------------------------------
            # Scenario A: Deterministic Setting (Temperature = 0.0)
            # -----------------------------------------------------------
            print("--- Scenario A: Low Temperature (temperature=0.0, deterministic) ---")
            config_deterministic = types.GenerateContentConfig(
                temperature=0.0,
                max_output_tokens=50
            )
            for i in range(2):
                res = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt,
                    config=config_deterministic
                )
                text = res.text.strip() if res.text else "[Factual response generated]"
                print(f"  Run #{i+1}: {text}")

            # -----------------------------------------------------------
            # Scenario B: Creative Setting (Temperature = 1.0)
            # -----------------------------------------------------------
            print("\n--- Scenario B: High Temperature (temperature=1.0, creative) ---")
            config_creative = types.GenerateContentConfig(
                temperature=1.0,
                max_output_tokens=50
            )
            for i in range(2):
                res = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt,
                    config=config_creative
                )
                text = res.text.strip() if res.text else "[Creative response generated]"
                print(f"  Run #{i+1}: {text}")

            # -----------------------------------------------------------
            # Scenario C: Token Capping (max_output_tokens = 15)
            # -----------------------------------------------------------
            print("\n--- Scenario C: Strict Token Cap (max_output_tokens=15) ---")
            long_prompt = "Provide a comprehensive plot overview of the novel 'Dune'."
            config_capped = types.GenerateContentConfig(
                temperature=0.2,
                max_output_tokens=15
            )
            res_capped = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=long_prompt,
                config=config_capped
            )
            text_out = res_capped.text.strip() if res_capped.text else "[Max tokens reached before completion]"
            print(f"  Capped Output: \"{text_out}\"")
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
