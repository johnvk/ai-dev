from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

# Zero-shot — just ask directly, no examples
messages = [
    SystemMessage(content="You are a helpful insurance support assistant."),
    HumanMessage(content="Classify this ticket as URGENT, NORMAL or LOW: 'My app has been down for 2 hours!'")
]

response = llm.invoke(messages)
print("Zero-shot result:", response.content)

# Few-shot — give examples to guide the output
few_shot_messages = [
    SystemMessage(content="""You are an insurance support ticket classifier.
Classify tickets as URGENT, NORMAL or LOW.
Only respond with the classification word, nothing else.

Examples:
Ticket: 'System is completely down' → URGENT
Ticket: 'Can I update my email address?' → LOW
Ticket: 'My claim from last week has no update' → NORMAL
"""),
    HumanMessage(content="Classify this ticket: 'My payment failed twice today and I cant access my policy'")
]

response2 = llm.invoke(few_shot_messages)
print("Few-shot result:", response2.content)

# Chain-of-thought — ask it to think step by step
cot_messages = [
    SystemMessage(content="You are an insurance claims analyst."),
    HumanMessage(content="""A customer has a policy that covers max 2 claims per year.
They filed claims in January and March.
They are now filing a third claim in April.

Think step by step and determine if this third claim is valid.
""")
]

response3 = llm.invoke(cot_messages)
print("Chain-of-thought result:", response3.content)

# Structured output — force JSON response
import json

structured_messages = [
    SystemMessage(content="""You are an insurance support ticket classifier.
Analyse the ticket and return ONLY valid JSON with exactly these fields:
- category: one of [CLAIMS, BILLING, TECHNICAL, GENERAL]
- priority: one of [LOW, NORMAL, URGENT]
- suggested_response: a short 1-sentence reply to the customer

No explanation. No markdown. No code blocks. Raw JSON only."""),
    HumanMessage(content="Ticket: 'I submitted a claim 3 weeks ago and nobody has contacted me'")
]

response4 = llm.invoke(structured_messages)
print("Raw output:", response4.content)

# Now parse it as real JSON
parsed = json.loads(response4.content)
print("\nParsed JSON:")
print(f"  Category : {parsed['category']}")
print(f"  Priority : {parsed['priority']}")
print(f"  Response : {parsed['suggested_response']}")