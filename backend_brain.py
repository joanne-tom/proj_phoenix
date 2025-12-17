
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage

# ==========================================
# 🔑 CONFIGURATION
# ==========================================
# REPLACE WITH YOUR REAL KEY
os.environ["GOOGLE_API_KEY"] = "AIzaSyCqpCTDrwKvv8aUJcBJZ_fWJS6PGNBhMSc" 

# ==========================================
# 🧠 REAL-TIME KNOWLEDGE BASE (Mocked for Speed)
# ==========================================
KNOWLEDGE_BASE = {
    "failed_cardio_drugs": [
        {"name": "Sildenafil", "status": "Failed Phase III", "original_indication": "Angina", "reason": "No significant improvement in blood flow."}
    ],
    "sildenafil_trials": [
        {"id": "NCT001", "phase": "Phase III", "notes": "Patients reported headaches, flushing, and prolonged erections."},
        {"id": "NCT002", "phase": "Phase II", "notes": "Side effect profile unusual for angina medication."}
    ],
    "market_data": {
        "erectile_dysfunction": {"size": "$10 Billion", "cagr": "8.5%", "competitors": "None (First Mover)"},
        "angina": {"size": "$500 Million", "cagr": "2%", "competitors": "High"}
    },
    "patents": {
        "sildenafil_angina": "EXPIRED",
        "sildenafil_ed": "AVAILABLE_FOR_FILING"
    }
}

# ==========================================
# 🛠️ MCP TOOLS
# ==========================================

@tool
def internal_database_search(query: str):
    """Searches internal company records for failed drugs."""
    return f"SEARCH RESULT: {KNOWLEDGE_BASE['failed_cardio_drugs']}"

@tool
def web_intelligence_search(query: str):
    """Searches clinical trial notes and patient forums."""
    if "sildenafil" in query.lower():
        return f"TRIAL NOTES: {KNOWLEDGE_BASE['sildenafil_trials']}"
    return "No significant signals found."

@tool
def iqvia_market_search(indication: str):
    """Queries IQVIA for market size and competition."""
    key = "erectile_dysfunction" if "erect" in indication.lower() else "angina"
    return f"MARKET REPORT: {KNOWLEDGE_BASE['market_data'].get(key, 'Unknown')}"

@tool
def patent_landscape_search(molecule: str, indication: str):
    """Checks patent availability."""
    if "sildenafil" in molecule.lower() and "erect" in indication.lower():
        return f"PATENT STATUS: {KNOWLEDGE_BASE['patents']['sildenafil_ed']}"
    return "PATENT STATUS: BLOCKED"

# ==========================================
# 🤖 THE AGENT BRAIN
# ==========================================

tools = [internal_database_search, web_intelligence_search, iqvia_market_search, patent_landscape_search]
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

# FIX: Remove 'state_modifier'/'messages_modifier' to avoid version errors
graph = create_react_agent(llm, tools) 

SYSTEM_INSTRUCTIONS = """
SYSTEM INSTRUCTIONS:
You are 'Project Phoenix', an expert Pharma R&D AI. 
Your goal: Find failed drugs that can be repurposed for high-value new markets.

STRATEGY:
1. Search internal DB for failed drugs.
2. Check their side effects (Web Search).
3. IF you find a weird side effect (like erections), PIVOT to that new market.
4. Check Market Size (IQVIA) and Patents for the NEW use.
5. Write a "Innovation Report" recommending the new use.
"""

def run_agent_backend(user_input):
    """
    Runs the REAL agent. We prepend the system instructions to the user input
    to guarantee the AI behaves correctly without needing special graph arguments.
    """
    # Prepend instructions to the user prompt
    augmented_prompt = f"{SYSTEM_INSTRUCTIONS}\n\nUSER REQUEST: {user_input}"
    
    inputs = {"messages": [("user", augmented_prompt)]}
    
    for s in graph.stream(inputs, stream_mode="values"):
        message = s["messages"][-1]
        yield message
