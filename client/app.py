import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from agent.orchestrator import UdaPlayOrchestrator

st.set_page_config(page_title="UdaPlay - AI Gaming Assistant", page_icon="🎮")
st.title("🎮 UdaPlay AI Research Agent")

@st.cache_resource
def load_orchestrator():
    return UdaPlayOrchestrator()

orchestrator = load_orchestrator()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about video games..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing gaming databases & search networks..."):
            output = orchestrator.route_and_execute(prompt)
            response_text = output["final_response"]
            st.markdown(response_text)
            
            with st.expander("Show Execution Telemetry"):
                st.write(f"**Selected Source:** {output['source_type']}")
                st.text_area("Retrieved Context", output["context"], height=150)

    st.session_state.messages.append({"role": "assistant", "content": response_text})
