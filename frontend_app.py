import streamlit as st
import pandas as pd
import plotly.express as px  # <--- NEW IMPORT
from backend_brain import run_agent_backend
import re

# --- UI CONFIGURATION ---
st.set_page_config(page_title="Project Phoenix", layout="wide", page_icon="💊")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .success-box { padding: 15px; background-color: #1c4f2e; border-radius: 5px; border-left: 5px solid #00ff00; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("Project Phoenix")
    st.caption("powered by Gemini & LangGraph")
    st.divider()
    st.success("✅ Internal DB Connected")
    st.success("✅ IQVIA Market Data Connected")
    st.success("✅ USPTO Patents Connected")
    st.info("Agent Status: **ONLINE**")

# --- MAIN CHAT ---
st.title("💊 In-Depth Drug Analyser")
st.markdown("Ask the Master Agent to scout for repurposing opportunities.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        # Check if this message had a chart attached
        if isinstance(msg, dict) and "chart_data" in msg:
            st.plotly_chart(msg["chart_data"], key=f"hist_{msg['content'][:5]}")

def strip_markdown(md_text):
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', md_text)  # bold
    text = re.sub(r'\*(.*?)\*', r'\1', text)         # italics
    text = re.sub(r'\n\s*\*\s*', '\n- ', text)       # bullets
    return text

# --- INPUT ---
if prompt := st.chat_input("Enter R&D Query..."):
    # 1. User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. AI Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        chart_to_save = None
        
        with st.spinner("Agent is reasoning..."):
            # STREAM THE REAL STEPS
            for step in run_agent_backend(prompt):
                
                # A. Handle Tool Calls
                if hasattr(step, 'tool_calls') and len(step.tool_calls) > 0:
                    for tool_call in step.tool_calls:
                        tool_name = tool_call['name']
                        tool_args = tool_call['args']
                        with st.expander(f"🤖 Action: Calling {tool_name}..."):
                            # Format: key=value key2=value2
                            if isinstance(tool_args, dict):
                                args_str = " ".join(f"{k}={v}" for k, v in tool_args.items())
                            else:
                                args_str = str(tool_args)
                            st.write(args_str)

                            
                            # --- 📊 THE NEW FIGURE MODEL (CHART) ---
                            # If the agent is checking Market Data, show a Chart!
                            if tool_name == "iqvia_market_search":
                                st.write("📊 **Generating IQVIA Market Analysis...**")
                                
                                # Create a Mock DataFrame for the Visualization
                                df = pd.DataFrame({
                                    "Indication": ["Angina (Original)", "Erectile Dysfunction (New)"],
                                    "Market Size (Billions)": [0.5, 10.0],
                                    "Growth Rate": ["2%", "8.5%"]
                                })
                                
                                fig = px.bar(
                                    df, 
                                    x="Indication", 
                                    y="Market Size (Billions)", 
                                    color="Indication",
                                    title="Market Opportunity Comparison",
                                    text="Growth Rate",
                                    color_discrete_sequence=["#FF6B6B", "#4ECDC4"]
                                )
                                fig.update_layout(template="plotly_dark")
                                st.plotly_chart(fig)
                                chart_to_save = fig # Save for history
                
                # B. Handle Content
                elif hasattr(step, "content") and step.content:
                    # Normalise step.content to a string
                    if isinstance(step.content, list):
                        # LangChain messages often come as list of {"type": "text", "text": "..."}
                        parts = []
                        for c in step.content:
                            if isinstance(c, dict) and "text" in c:
                                parts.append(c["text"])
                            else:
                                parts.append(str(c))
                        raw_text = "\n".join(parts)
                    else:
                        raw_text = str(step.content)

                    clean_text = strip_markdown(raw_text)
                    message_placeholder.text_area("AI Output", value=clean_text, height=300)
                    full_response += clean_text + "\n\n"


        # Highlight Success
        if "Sildenafil" in full_response or "Innovation" in full_response:
             st.markdown('<div class="success-box"><h3>🚀 Opportunity Detected</h3></div>', unsafe_allow_html=True)
    
    # Save History (With Chart if it exists)
    msg_obj = {"role": "assistant", "content": full_response}
    if chart_to_save:
        msg_obj["chart_data"] = chart_to_save
    
    st.session_state.messages.append(msg_obj)
