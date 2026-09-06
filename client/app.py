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
    # 1. Store and display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing gaming databases & search networks..."):
            # 2. Run the orchestrator
            output = orchestrator.route_and_execute(prompt)
            raw_response = output["final_response"]
            
            # --- OPTION 1 EXTRACTION LOGIC ---
            # Check if the response is a list (with structured metadata) or a plain string
            if isinstance(raw_response, list):
                extracted_texts = [
                    item['text'] 
                    for item in raw_response 
                    if isinstance(item, dict) and item.get('type') == 'text' and 'text' in item
                ]
                # Join messages together, or take the first one
                response_text = "\n\n".join(extracted_texts) if extracted_texts else "No text found in response."
            else:
                # Fallback if it is already a plain string
                response_text = str(raw_response)
            # ----------------------------------

            # 3. Render the clean text to the UI
            st.markdown(response_text)
            
            # 4. Show debug/telemetry expander
            with st.expander("Show Execution Telemetry"):
                st.write(f"**Selected Source:** {output['source_type']}")
                st.text_area("Retrieved Context", output["context"], height=150)

    # 5. Append clean string to session state so history stays clean
    st.session_state.messages.append({"role": "assistant", "content": response_text})
