"""
Week 5 Project — Interactive CLI Library Knowledge Assistant
Allows you to interactively ask questions directly from the terminal!
"""
import sys
from main import ask_question, AskRequest


def main():
    print("\n" + "=" * 65)
    print(" 📚 WELCOME TO YOUR LIBRARY KNOWLEDGE ASSISTANT (RAG CLI)")
    print("=" * 65)
    print("Ask any question about your book catalog (e.g., sci-fi books,")
    print("database architecture, software engineering, or clean code).")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        try:
            user_query = input("💬 Ask a question: ").strip()
            if not user_query:
                continue
            if user_query.lower() in ["exit", "quit", "q"]:
                print("\nGoodbye! 👋 Happy learning!\n")
                break

            print("\n🔍 Searching library vector database & synthesizing answer...")
            req = AskRequest(question=user_query)
            response = ask_question(req)

            print("\n" + "-" * 65)
            print(f"📖 Answer:\n{response.answer}")
            print("-" * 65)
            if response.sources:
                print(f"📑 Sources: {', '.join(response.sources)}")
            else:
                print("📑 Sources: None (Grounding refusal)")
            print("=" * 65 + "\n")

        except (KeyboardInterrupt, EOFError):
            print("\n\nGoodbye! 👋\n")
            sys.exit(0)


if __name__ == "__main__":
    main()
