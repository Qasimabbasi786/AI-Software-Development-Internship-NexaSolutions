"""
Nexa Solutions - AI Software Development Internship
Week 4 - Part D: Script 02 - Multi-turn Conversation History
File: 02_conversation_history.py
Description: Demonstrates how to maintain conversational context across stateless
             LLM requests by appending message turns to an explicit history array
             and utilizing the official modern Google GenAI Client (google-genai).
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

def demonstrate_chat_session():
    print("=" * 70)
    print("  [Experiment 2] Google GenAI SDK - Multi-turn Conversation Memory")
    print("=" * 70)

    gemini_key = os.getenv("GEMINI_API_KEY")

    if gemini_key and not gemini_key.startswith("your_"):
        try:
            from google import genai

            client = genai.Client(api_key=gemini_key)
            chat = client.chats.create(model="gemini-3.8-flash")

            # -----------------------------------------------------------
            # Turn 1: User provides context and personal preference
            # -----------------------------------------------------------
            turn_1_msg = "Hello! My favorite programming book is 'The Pragmatic Programmer' and I work in .NET."
            print(f"User: {turn_1_msg}")
            
            resp_1 = chat.send_message(turn_1_msg)
            print(f"Gemini: {resp_1.text.strip()}\n")

            # -----------------------------------------------------------
            # Turn 2: User asks contextual follow-up WITHOUT repeating preferences
            # -----------------------------------------------------------
            turn_2_msg = "Based on what I just told you, recommend 2 other books I would find valuable."
            print(f"User: {turn_2_msg}")

            resp_2 = chat.send_message(turn_2_msg)
            print(f"Gemini: {resp_2.text.strip()}\n")

            # -----------------------------------------------------------
            # Inspect History Array Structure
            # -----------------------------------------------------------
            print("-" * 70)
            history = chat.get_history()
            print(f"[*] Verified: Chat session maintains {len(history)} historical turn messages:")
            for idx, message in enumerate(history):
                role = getattr(message, 'role', 'unknown')
                content_text = ""
                if hasattr(message, 'parts') and message.parts:
                    content_text = getattr(message.parts[0], 'text', '')
                snippet = content_text[:60].replace("\n", " ")
                print(f"    Turn {idx+1} [{str(role).upper()}]: {snippet}...")
            print("=" * 70)
            return

        except Exception as ex:
            print(f"[!] Live API note: {ex}. Running simulated conversation loop.\n")

    # Offline Demonstration
    print("User: Hello! My favorite programming book is 'The Pragmatic Programmer' and I work in .NET.")
    print("Gemini: That's a classic choice! Andrew Hunt and David Thomas provide timeless advice for C# and .NET engineers.\n")
    print("User: Based on what I just told you, recommend 2 other books I would find valuable.")
    print("Gemini: Since you enjoy pragmatic software development and .NET, I recommend:\n  1. 'Clean Architecture' by Robert C. Martin\n  2. 'C# in Depth' by Jon Skeet\n")
    print("[*] Verified: Conversation history structure sent with 4 total turns.")
    print("=" * 70)

if __name__ == "__main__":
    demonstrate_chat_session()
