"""
Nexa Solutions - AI Software Development Internship
Week 4 - Part D: Script 03 - Streaming Responses
File: 03_streaming.py
Description: Demonstrates chunk-by-chunk token streaming using Google Gemini API
             to dramatically reduce perceived user latency compared to waiting
             for complete responses.
"""

import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv

# Ensure UTF-8 output formatting for Windows console
if sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

def demonstrate_streaming():
    print("=" * 70)
    print("  [Experiment 3] Google Gemini API - Real-Time Token Streaming")
    print("=" * 70)

    gemini_key = os.getenv("GEMINI_API_KEY")
    prompt = (
        "In two clear, professional sentences, explain why server-side token streaming "
        "improves user experience (UX) in AI web applications."
    )

    print(f"[*] Prompt: \"{prompt}\"")
    print("[*] Initiating live token stream:\n")

    if gemini_key and not gemini_key.startswith("your_"):
        try:
            import google.generativeai as genai
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel("gemini-3.8-flash")

            start_time = time.time()
            response = model.generate_content(prompt, stream=True)

            first_token_time = None
            total_chunks = 0

            print("Stream Output: ", end="", flush=True)
            for chunk in response:
                if first_token_time is None:
                    first_token_time = time.time() - start_time
                total_chunks += 1
                print(chunk.text, end="", flush=True)

            total_duration = time.time() - start_time
            print("\n\n" + "-" * 70)
            print(f"[*] Latency Metrics:")
            print(f"    Time-to-First-Token (TTFT): {first_token_time:.2f} seconds")
            print(f"    Total Stream Duration:       {total_duration:.2f} seconds")
            print(f"    Total Chunks Delivered:      {total_chunks}")
            print("=" * 70)
            return

        except Exception as ex:
            print(f"\n[!] Live API note: {ex}. Running educational streaming simulation.\n")

    # Offline Demonstration
    simulated_text = (
        "Server-side token streaming delivers generated words progressively, "
        "allowing users to begin reading within milliseconds instead of waiting "
        "for the complete response to compile. This dramatically diminishes "
        "perceived latency and creates an interactive, highly responsive application feel."
    )

    print("Stream Output: ", end="", flush=True)
    for word in simulated_text.split(" "):
        print(word + " ", end="", flush=True)
        time.sleep(0.04)

    print("\n\n" + "-" * 70)
    print("[*] Latency Metrics (Simulated):")
    print("    Time-to-First-Token (TTFT): 0.18 seconds")
    print("    Total Stream Duration:       1.85 seconds")
    print("=" * 70)

if __name__ == "__main__":
    demonstrate_streaming()
