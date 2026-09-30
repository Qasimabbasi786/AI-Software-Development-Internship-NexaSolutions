"""
Week 3 - AI Script: Standalone Python Script
File: summarize_book.py
Description: Takes a book title and description, queries Google Gemini API
             (e.g., gemini-1.5-flash or gemini-2.0-flash) for a concise summary
             and genre suggestion, and prints the result to the console.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Ensure standard UTF-8 stream output for Windows console
if sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

# 1. Load environment variables securely from .env located inside ai-services folder
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

def generate_book_summary(title: str, description: str):
    print("=" * 65)
    print(f" [*] Book Title : {title}")
    print(f" [*] Description: {description}")
    print("-" * 65)

    gemini_api_key = os.getenv("GEMINI_API_KEY")

    if not gemini_api_key or gemini_api_key == "your_actual_gemini_api_key_here":
        print("[!] Note: GEMINI_API_KEY is not configured or using placeholder in ai-services/.env.")
        print("    Running in demonstration mode with synthesized LLM response:\n")
        print("[AI Summary & Genre Recommendation - Fallback Demonstration]")
        print(f"Summary: '{title}' is a poignant literary work delving deeply into human resilience,")
        print("cultural heritage, and progressive thought. Through evocative storytelling, it captures")
        print("both historical moments and personal transformations.")
        print("Suggested Genres: [Urdu Literature, Poetry / Classical, Cultural History]\n")
        return

    try:
        import google.generativeai as genai

        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel("gemini-flash-latest")

        prompt = (
            f"You are an expert literature assistant. Please provide a concise one-paragraph summary "
            f"and suggest 3 relevant literary genres for the book titled '{title}' with description: '{description}'."
        )

        response = model.generate_content(prompt)
        print("[*] Google Gemini AI Response:")
        print(response.text.strip())
        print("\n" + "=" * 65)
    except ImportError:
        print("[!] Error: 'google-generativeai' package is not installed.")
        print("    Run: pip install -r requirements.txt")
    except Exception as ex:
        print(f"[!] Error calling Google Gemini API: {ex}")

if __name__ == "__main__":
    test_title = sys.argv[1] if len(sys.argv) > 1 else "Nuskha-Hai-Wafa"
    test_desc = (
        sys.argv[2]
        if len(sys.argv) > 2
        else "Faiz Ahmed Faiz poetry collection covering themes of love, struggle, and justice."
    )
    generate_book_summary(test_title, test_desc)

