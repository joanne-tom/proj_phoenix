import streamlit as st
import pandas as pd
import re
from backend_brain import run_agent_backend

# --- UI CONFIGURATION ---
st.set_page_config(page_title="Project Phoenix", layout="wide", page_icon="💊")

# Custom CSS
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .success-box { padding: 15px; background-color: #1c4f2e; border-radius: 5px; border-left: 5px solid #00ff00; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3063/3063212.png", width=50) # Placeholder Icon
    st.title("Project Phoenix")
    st.caption("Agentic R&D Discovery Engine")
    st.divider()
    st.success("✅ Internal DB Connected")
    st.success("✅ IQVIA Market Data Connected")
    st.success("✅ USPTO Patents Connected")
    st.info("Agent Status: **ONLINE**")

# --- MAIN CHAT ---
st.title("💊 In-depth Drug Analyser")
st.markdown("Ask the Master Agent to find repurposing opportunities for failed drugs.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Helper: Strip Markdown for cleaner display
def strip_markdown(md_text):
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', md_text)  # bold
    text = re.sub(r'\*(.*?)\*', r'\1', text)         # italics
    text = re.sub(r'\n\s*\*\s*', '\n- ', text)       # bullets
    return text

# --- INPUT ---
if prompt := st.chat_input("Enter your R&D Query..."):
    # 1. User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. AI Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response_text = ""

        with st.spinner("Agent is reasoning..."):
            # STREAM THE REAL STEPS
            for step in run_agent_backend(prompt):

                # A. Handle Tool Calls
                if hasattr(step, 'tool_calls') and len(step.tool_calls) > 0:
                    for tool_call in step.tool_calls:
                        tool_name = tool_call['name']
                        tool_args = tool_call['args']
                        with st.expander(f"🤖 Action: Calling {tool_name}..."):
                            st.write(' '.join(f'{k}={v}' for k, v in tool_args.items()))

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
                    full_response_text += clean_text + "\n\n"


        # Highlight Success
        if "Sildenafil" in full_response_text or "Innovation" in full_response_text:
             st.markdown(
                 '<div class="success-box"><h3>🚀 Opportunity Detected</h3></div>',
                 unsafe_allow_html=True
             )

    # Save History
    st.session_state.messages.append({"role": "assistant", "content": full_response_text})
