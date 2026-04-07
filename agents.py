from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langchain.agents import create_agent

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

# --- TOOLS ---
@tool
def get_claim_status(claim_id: str) -> str:
    """Look up the current status of an insurance claim by claim ID.
    Use this when the user asks about a claim status."""
    fake_claims = {
        "1234": {"status": "APPROVED", "filed_date": "2026-03-01", "amount": "$2,500"},
        "5678": {"status": "PENDING", "filed_date": "2026-03-28", "amount": "$800"},
        "9999": {"status": "REJECTED", "filed_date": "2026-02-15", "amount": "$1,200"},
    }
    claim = fake_claims.get(claim_id)
    if claim:
        return f"Claim {claim_id}: Status={claim['status']}, Filed={claim['filed_date']}, Amount={claim['amount']}"
    return f"Claim {claim_id} not found."

@tool
def get_policy_details(policy_id: str) -> str:
    """Retrieve policy details for a given policy ID.
    Use this when the user asks about their policy coverage or details."""
    fake_policies = {
        "POL001": {"type": "Comprehensive", "expiry": "2027-01-01", "premium": "$120/month"},
        "POL002": {"type": "Third Party", "expiry": "2026-12-01", "premium": "$60/month"},
    }
    policy = fake_policies.get(policy_id)
    if policy:
        return f"Policy {policy_id}: Type={policy['type']}, Expiry={policy['expiry']}, Premium={policy['premium']}"
    return f"Policy {policy_id} not found."

@tool
def calculate_premium(vehicle_age: int, claim_history: int) -> str:
    """Calculate estimated monthly premium based on vehicle age and number of past claims.
    Use this when the user wants a premium estimate."""
    base = 100
    age_factor = vehicle_age * 5
    claim_factor = claim_history * 20
    total = base + age_factor + claim_factor
    return f"Estimated monthly premium: ${total} (Base: $100, Age factor: ${age_factor}, Claims factor: ${claim_factor})"

# --- AGENT SETUP using LangGraph ---
tools = [get_claim_status, get_policy_details, calculate_premium]

# create_react_agent from LangGraph is the modern way
agent = create_react_agent(llm, tools)

def run_agent(question):
    print(f"\nQ: {question}")
    result = agent.invoke({
        "messages": [HumanMessage(content=question)]
    })
    # Get the last message which is the final answer
    print(f"A: {result['messages'][-1].content}")

# Test 1 — Claim lookup
run_agent("What is the status of claim #1234?")

# Test 2 — Policy details
run_agent("Can you show me details for policy POL001?")

# Test 3 — Premium calculation
run_agent("Calculate my premium, my car is 3 years old and I have 2 past claims")

# Test 4 — Multi-step reasoning
run_agent("Check claim #5678 and also calculate premium for a 5 year old car with 1 claim")