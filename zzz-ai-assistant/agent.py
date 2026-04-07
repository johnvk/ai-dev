from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.prebuilt import create_react_agent
from tools import all_tools
from rag import build_vectorstore, build_rag_tool

def build_agent():
    print("🤖 Building ZZZ Insurance AI Assistant...")

    # Step 1 — Build RAG vectorstore and tool
    vectorstore = build_vectorstore()
    rag_tool = build_rag_tool(vectorstore)

    # Step 2 — Combine RAG tool with all other tools
    tools = all_tools + [rag_tool]

    # Step 3 — Setup LLM
    llm = ChatOpenAI(model="gpt-4o-mini")

    # Step 4 — Create agent
    agent = create_react_agent(llm, tools)
    print("   Agent ready ✅\n")

    return agent

def run_agent(agent, question, chat_history):
    # Build messages — history + current question
    messages = chat_history + [HumanMessage(content=question)]

    result = agent.invoke({"messages": messages})

    # Extract final answer
    answer = str(result["messages"][-1].content)

    # Update history
    chat_history.append(HumanMessage(content=question))
    chat_history.append(AIMessage(content=answer))

    return answer