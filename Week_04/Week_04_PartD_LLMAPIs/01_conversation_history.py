"""
Week 4 - Part D: Multi-turn Conversation History
Demonstrates maintaining state across stateless Google Gemini API calls.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

def run_conversation_demo():
    print("=== Multi-turn Conversation State Demo (Google Gemini) ===")
    
    gemini_key = os.getenv("GEMINI_API_KEY")

    if gemini_key and not gemini_key.startswith("your_"):
        try:
            import google.generativeai as genai
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            chat = model.start_chat(history=[])

            # Turn 1
            print("User: Hello! My favorite book is 'The Pragmatic Programmer' and I love Clean Code.")
            resp1 = chat.send_message("Hello! My favorite book is 'The Pragmatic Programmer' and I love Clean Code.")
            print(f"Gemini: {resp1.text.strip()}\n")

            # Turn 2 - Chat session automatically preserves history
            print("User: Can you recommend two more books similar to my favorite ones?")
            resp2 = chat.send_message("Can you recommend two more books similar to my favorite ones?")
            print(f"Gemini: {resp2.text.strip()}\n")
            print(f"Total message turns in chat history: {len(chat.history)}")
            return
        except Exception as ex:
            print(f"[!] Live API note: {ex}. Running simulated conversation loop.\n")

    # Offline / Architectural Demonstration
    history = [
        {"role": "user", "parts": ["Hello! My favorite book is 'The Pragmatic Programmer' and I love Clean Code."]}
    ]
    print("User: Hello! My favorite book is 'The Pragmatic Programmer' and I love Clean Code.")
    print("Gemini: [Model generates reply acknowledging your favorite software architecture books]\n")
    
    history.append({
        "role": "model",
        "parts": ["Nice to meet you! 'The Pragmatic Programmer' and 'Clean Code' are essential classics."]
    })
    
    # Second turn - the model needs the entire history array resent
    history.append({
        "role": "user",
        "parts": ["Can you recommend two more books similar to my favorite ones?"]
    })
    
    print("User: Can you recommend two more books similar to my favorite ones?")
    print("--> Entire message history is sent to Google Gemini to maintain contextual memory.")
    print(f"Total history payload items: {len(history)}")

if __name__ == "__main__":
    run_conversation_demo()
