from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI developer coach helping {name} learn AI development."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{question}")
])

chain = prompt | llm

chat_history = []

print("🤖 AI Coach ready! Type 'quit' to exit\n")

name = input("What's your name? ")

while True:
    user_input = input("\nYou: ")

    if user_input.lower() == "quit":
        print("Goodbye! Keep coding! 🚀")
        break

    response = chain.invoke({
        "name": name,
        "question": user_input,
        "chat_history": chat_history
    })

    answer = str(response.content)

    chat_history.append(HumanMessage(content=user_input))
    chat_history.append(AIMessage(content=answer))

    print(f"\n🤖 Coach: {answer}")