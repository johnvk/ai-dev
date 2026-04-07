from langchain_core.tools import tool

# --- CLAIM TOOL ---
@tool
def get_claim_status(claim_id: str) -> str:
    """Look up the current status of a ZZZ Insurance claim by claim ID.
    Use this when the user asks about a claim status or claim update."""
    claims = {
        "1234": {"status": "APPROVED", "filed_date": "2026-03-01", "amount": "$2,500"},
        "5678": {"status": "PENDING",  "filed_date": "2026-03-28", "amount": "$800"},
        "9999": {"status": "REJECTED", "filed_date": "2026-02-15", "amount": "$1,200"},
    }
    claim = claims.get(claim_id)
    if claim:
        return (f"Claim {claim_id}: Status={claim['status']}, "
                f"Filed={claim['filed_date']}, Amount={claim['amount']}")
    return f"Claim {claim_id} not found in the system."

# --- POLICY TOOL ---
@tool
def get_policy_details(policy_id: str) -> str:
    """Retrieve ZZZ Insurance policy details for a given policy ID.
    Use this when the user asks about their policy, coverage, or expiry."""
    policies = {
        "POL001": {"type": "Comprehensive", "expiry": "2027-01-01", "premium": "$120/month"},
        "POL002": {"type": "Third Party",   "expiry": "2026-12-01", "premium": "$60/month"},
        "POL003": {"type": "Comprehensive", "expiry": "2026-09-15", "premium": "$140/month"},
    }
    policy = policies.get(policy_id)
    if policy:
        return (f"Policy {policy_id}: Type={policy['type']}, "
                f"Expiry={policy['expiry']}, Premium={policy['premium']}")
    return f"Policy {policy_id} not found in the system."

# --- PREMIUM CALCULATOR TOOL ---
@tool
def calculate_premium(vehicle_age: int, claim_history: int) -> str:
    """Calculate estimated monthly premium for ZZZ Insurance
    based on vehicle age (years) and number of past claims.
    Use this when the user wants a premium estimate or quote."""
    base = 100
    age_factor = vehicle_age * 5
    claim_factor = claim_history * 20
    total = base + age_factor + claim_factor
    return (f"Estimated monthly premium: ${total} "
            f"(Base: $100, Age factor: ${age_factor}, "
            f"Claims factor: ${claim_factor})")

# --- CONTACT TOOL ---
@tool
def get_contact_info(department: str) -> str:
    """Get ZZZ Insurance contact information for a specific department.
    Use this when the user asks how to contact ZZZ Insurance or needs
    a phone number or email."""
    contacts = {
        "claims":   {"phone": "1800-ZZZ-CLAIMS", "email": "claims@zzzinsurance.com.au"},
        "billing":  {"phone": "1800-ZZZ-BILLING", "email": "billing@zzzinsurance.com.au"},
        "general":  {"phone": "1800-ZZZ-HELP",   "email": "help@zzzinsurance.com.au"},
        "emergency":{"phone": "1800-ZZZ-SOS",    "email": "emergency@zzzinsurance.com.au"},
    }
    dept = contacts.get(department.lower())
    if dept:
        return f"{department.title()} Dept: Phone={dept['phone']}, Email={dept['email']}"
    return f"Department '{department}' not found. Try: claims, billing, general, emergency."

# All tools in one list for easy import
all_tools = [get_claim_status, get_policy_details, calculate_premium, get_contact_info]