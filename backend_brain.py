# #backend
# import os
# import time
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.tools import tool
# from langgraph.prebuilt import create_react_agent
# from langchain_core.messages import SystemMessage

# # --- 1. CONFIGURATION ---
# # PASTE YOUR GOOGLE API KEY HERE
# # Get it for free at: https://aistudio.google.com/app/apikey
# os.environ["GOOGLE_API_KEY"] = "AIzaSy..." # <--- REPLACE THIS WITH YOUR ACTUAL KEY

# # --- 2. MOCK DATA (The "Golden Source") ---
# # This ensures your demo works 100% of the time.
# MOCK_DB = {
#     "failed_cardio_drugs": [
#         {"name": "Sildenafil", "status": "Failed Phase III", "original_indication": "Angina", "reason": "No significant improvement in blood flow."}
#     ],
#     "sildenafil_trials": [
#         {"id": "NCT001", "phase": "Phase III", "notes": "Patients reported headaches, flushing, and prolonged erections."},
#         {"id": "NCT002", "phase": "Phase II", "notes": "Side effect profile unusual for angina medication."}
#     ],
#     "market_data": {
#         "erectile_dysfunction": {"size": "$10 Billion", "cagr": "8.5%", "competitors": "None (First Mover)"},
#         "angina": {"size": "$500 Million", "cagr": "2%", "competitors": "High"}
#     },
#     "patents": {
#         "sildenafil_angina": "EXPIRED",
#         "sildenafil_ed": "AVAILABLE_FOR_FILING"
#     }
# }

# # --- 3. THE "MCP" TOOLS (Connected to Mock Data) ---

# @tool
# def internal_database_search(query: str):
#     """Searches internal company records for failed drugs."""
#     # We force the result to ensure the demo flows correctly
#     return f"FOUND: {MOCK_DB['failed_cardio_drugs']}"

# @tool
# def web_intelligence_search(query: str):
#     """Searches clinical trial notes and patient forums."""
#     if "sildenafil" in query.lower():
#         return f"TRIAL NOTES: {MOCK_DB['sildenafil_trials']}"
#     return "No significant signals found."

# @tool
# def iqvia_market_search(indication: str):
#     """Queries IQVIA for market size and competition."""
#     # Simple logic to return the right mock data
#     key = "erectile_dysfunction" if "erect" in indication.lower() else "angina"
#     return f"MARKET REPORT: {MOCK_DB['market_data'].get(key, 'Unknown')}"

# @tool
# def patent_landscape_search(molecule: str, indication: str):
#     """Checks patent availability."""
#     if "sildenafil" in molecule.lower() and "erect" in indication.lower():
#         return f"PATENT STATUS: {MOCK_DB['patents']['sildenafil_ed']}"
#     return "PATENT STATUS: BLOCKED"

# # --- 4. THE ORCHESTRATOR (Gemini Powered) ---

# # We tell Gemini exactly how to behave
# system_prompt = """
# You are 'Project Phoenix', an elite R&D Strategist AI.
# Your goal is to find 'contrarian' drug repurposing opportunities.

# FOLLOW THIS EXACT THOUGHT PROCESS:
# 1. Search internal databases for failed drugs (use 'internal_database_search').
# 2. Investigate their side effects using 'web_intelligence_search'.
# 3. IF you find a side effect like 'erections', PIVOT immediately.
# 4. Check the market size for that *new* side effect (indication) using 'iqvia_market_search'.
# 5. Check patent availability using 'patent_landscape_search'.
# 6. Compile a final 'Innovation Report' as your final answer.

# Keep your responses concise and professional.
# """

# # Define the tools
# tools = [internal_database_search, web_intelligence_search, iqvia_market_search, patent_landscape_search]

# # Initialize Gemini 1.5 Flash (Free & Fast)
# llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)

# # Create the Agent Graph
# graph = create_react_agent(llm, tools, messages_modifier=system_prompt)

# def run_agent(user_input):
#     """Runs the agent and returns the conversation history."""
#     inputs = {"messages": [("user", user_input)]}
#     response = []
    
#     # Run the agent
#     # We use stream_mode="values" to get the full message history updates
#     for s in graph.stream(inputs, stream_mode="values"):
#         message = s["messages"][-1]
        
#         # Format the output for our Frontend
#         if hasattr(message, 'tool_calls') and len(message.tool_calls) > 0:
#             for tool_call in message.tool_calls:
#                 response.append({
#                     "type": "tool",
#                     "name": tool_call['name'],
#                     "args": tool_call['args'],
#                     "result": "Processing..." # The result comes in the next message
#                 })
#         elif hasattr(message, 'content') and message.content:
#              # This is a text response (Thought or Final Answer)
#              if "Innovation Report" in message.content:
#                  response.append({"type": "final", "content": message.content})
#              else:
#                  # It's a "thought" if it's not the final report
#                  response.append({"type": "thought", "content": message.content})
        
#     return response

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
