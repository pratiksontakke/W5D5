import streamlit as st
import sys
import os

# --- PATH SETUP ---
# This is a crucial step to ensure the app can find the 'app' module
# It adds the project's root directory to Python's path
# Assumes the script is run from the 'sql_rag_agent' directory
try:
    # This block handles the path when running `streamlit run frontend/ui.py`
    # from the root 'sql_rag_agent' directory.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, '..'))
    sys.path.append(project_root)
    from app.agent import get_answer
except ImportError:
    # This block is a fallback for different execution environments
    # It assumes 'app' is in the python path
    try:
        from app.agent import get_answer
    except ImportError as e:
        st.error(f"Error importing agent: {e}. Make sure you are running Streamlit from the 'sql_rag_agent' root directory.")
        st.stop()


# --- STREAMLIT APP CONFIGURATION ---
st.set_page_config(page_title="Customer Support AI", layout="wide")

st.title("🤖 AI Customer Support Assistant")
st.caption("Ask me about customer support tickets. I can find specific data or search for solutions.")


# --- CHAT HISTORY INITIALIZATION ---
# This uses the session state to keep the chat history persistent
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How can I help you today?"}]


# --- DISPLAY CHAT MESSAGES ---
# This loop iterates through the saved messages and displays them
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# --- USER INPUT HANDLING ---
# The st.chat_input widget waits for the user to enter a message
if prompt := st.chat_input("Ask a question..."):
    # 1. Add user's message to history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Get the assistant's response
    with st.chat_message("assistant"):
        # Show a "thinking" spinner while the agent processes the query
        with st.spinner("Thinking..."):
            response = get_answer(prompt)
            st.markdown(response)

    # 3. Add assistant's response to history
    st.session_state.messages.append({"role": "assistant", "content": response})