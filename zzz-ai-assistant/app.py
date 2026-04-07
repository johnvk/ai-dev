import os
from dotenv import load_dotenv
from agent import build_agent, run_agent

load_dotenv()

def main():
    # Header
    print("=" * 50)
    print("   ZZZ Insurance AI Assistant")
    print("=" * 50)
    print("Type 'quit' to exit\n")

    # Build the agent (loads RAG + tools)
    agent = build_agent()

    # Chat history for memory
    chat_history = []

    # Greet the user
    name = input("Welcome! What's your name? ")
    print(f"\nHello {name}! I'm your ZZZ Insurance assistant.")
    print("I can help you with:")
    print("  • Policy questions")
    print("  • Claim status")
    print("  • Premium calculations")
    print("  • Contact information")
    print("\nHow can I help you today?\n")
    print("-" * 50)

    # Main chat loop
    while True:
        user_input = input(f"\n{name}: ").strip()

        if not user_input:
            continue

        if user_input.lower() == "quit":
            print(f"\nThank you for using ZZZ Insurance Assistant. Goodbye {name}! 👋")
            break

        print("\n🤖 Assistant: ", end="", flush=True)
        response = run_agent(agent, user_input, chat_history)
        print(response)
        print("-" * 50)

if __name__ == "__main__":
    main()