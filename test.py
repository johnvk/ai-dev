from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")  # cheapest, fast, great for learning
response = llm.invoke("Say hello in one sentence.")
print(response.content)