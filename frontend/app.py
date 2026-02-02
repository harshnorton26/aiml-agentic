"""
HR Policy Assistant - Streamlit UI
"""

import streamlit as st
import sys
import os
from datetime import datetime

# Add parent directory to path for backend imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

st.set_page_config(page_title="HR Policy Assistant", page_icon="👔", layout="wide")

# Custom CSS
st.markdown("""
<style>
.user-msg {
    background: #e3f2fd;
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 0.5rem 0;
    margin-left: auto;
    margin-right: 0;
    max-width: 70%;
    text-align: left;
}
.asst-msg {
    background: #f5f5f5;
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 0.5rem 0;
    margin-left: 0;
    margin-right: auto;
    max-width: 70%;
    text-align: left;
}
.info-msg {
    background: #fff3e0;
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 0.5rem 0;
    border-left: 4px solid #ff9800;
}
.chat-container {
    max-height: 65vh;
    overflow-y: auto;
    padding: 1rem;
    margin-bottom: 1rem;
}
.title-header {
    margin-top: -2rem;
    margin-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'agent' not in st.session_state:
    st.session_state.agent = None
    st.session_state.agent_ready = False

if 'messages' not in st.session_state:
    st.session_state.messages = []

# Auto-initialize agent on page load
if not st.session_state.agent_ready:
    try:
        from backend import create_hr_agent
        with st.spinner("🚀 Loading HR Policy Agent... This may take 30-60 seconds on first load."):
            st.session_state.agent = create_hr_agent(model_name="mistral", verbose=False)
            st.session_state.agent_ready = True
    except Exception as e:
        st.error(f"❌ Failed to initialize agent: {str(e)}")
        st.info("Make sure Ollama is running: `ollama serve`")

# Sidebar - Settings and Controls
with st.sidebar:
    # Display active model
    if st.session_state.agent_ready:
        st.markdown("#### 🤖 Model")
        st.info("**Mistral** (via Ollama)")
    
    # Clear Chat Button
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        if st.session_state.agent:
            st.session_state.agent.reset_memory()
        st.rerun()
    
    st.divider()
    # st.markdown("### 💡 Example Questions")
    
    # examples = [
    #     "What is annual leave?",
    #     "Sick leave policy?",
    #     "Work from home rules?",
    #     "How many holidays?",
    # ]
    
    # for q in examples:
    #     if st.button(q, key=f"q_{q}", use_container_width=True):
    #         st.session_state.messages.append({"role": "user", "content": q})
    #         
    #         # Get agent response
    #         if st.session_state.agent_ready:
    #             with st.spinner("🤔 Thinking..."):
    #                 try:
    #                     response = st.session_state.agent.chat(q)
    #                     st.session_state.messages.append({"role": "assistant", "content": response})
    #                 except Exception as e:
    #                     st.session_state.messages.append({"role": "assistant", "content": f"❌ Error: {str(e)}"})
    #         
    #         st.rerun()

# Main Content
st.markdown('<div class="title-header"><h3>👔 HR Policy Assistant</h3></div>', unsafe_allow_html=True)

# Display Chat Messages in scrollable container
chat_html = '<div class="chat-container">'
for msg in st.session_state.messages:
    if msg["role"] == "user":
        chat_html += f'<div class="user-msg"><b>👤 You:</b> {msg["content"]}</div>'
    else:
        chat_html += f'<div class="asst-msg"><b>🤖 Assistant:</b> {msg["content"]}</div>'
chat_html += '</div>'
st.markdown(chat_html, unsafe_allow_html=True)

# Chat Input
user_input = st.chat_input("Ask about HR policies...", disabled=not st.session_state.agent_ready)

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    if st.session_state.agent_ready:
        with st.spinner("🤔 Thinking..."):
            try:
                response = st.session_state.agent.chat(user_input)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.session_state.messages.append({"role": "assistant", "content": f"❌ Error: {str(e)}"})
    else:
        st.error("⚠️ Initialize agent first!")
    
    st.rerun()
