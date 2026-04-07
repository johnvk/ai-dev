from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")
parser = StrOutputParser()

# Chain 1 — Classify the ticket
classify_prompt = ChatPromptTemplate.from_messages([
    ("system", """Classify this support ticket into one of these categories:
CLAIMS, BILLING, TECHNICAL, GENERAL.
Respond with just the category word, nothing else."""),
    ("user", "Ticket: {ticket}")
])

# Chain 2 — Generate a response based on the classification
respond_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a support assistant for NTI Insurance.
A ticket has been classified as {category}.
Write a short, professional 2-sentence response to the customer."""),
    ("user", "Original ticket: {ticket}")
])

# Build individual chains
classify_chain = classify_prompt | llm | parser | (lambda x: str(x))
respond_chain = respond_prompt | llm | parser | (lambda x: str(x))

# Run them sequentially
ticket = "I submitted my claim 3 weeks ago and have not heard back"

category = classify_chain.invoke({"ticket": ticket})
print("Category:", category)

response = respond_chain.invoke({
    "category": category,
    "ticket": ticket
})
print("Response:", response)

# Batch processing — run multiple tickets at once
tickets = [
    {"ticket": "My app has been down for 2 hours!"},
    {"ticket": "Can I update my email address?"},
    {"ticket": "My monthly premium is higher than quoted"},
    {"ticket": "I submitted a claim 3 weeks ago, no response"}
]

print("\n--- Batch Classification ---")
results = classify_chain.batch(tickets)
for ticket, category in zip(tickets, results):
    print(f"  {category:10} → {ticket['ticket']}")