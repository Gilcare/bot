import asyncio
import streamlit as st
from chatbot import initialize_parlant, get_response  # Import chatbot logic

# Function to handle chatbot interaction
def chatbot():
    # Check if Parlant session is initialized
    if "parlant_session" not in st.session_state:
        with st.spinner("Initializing Kyma..."):
            # Initialize Parlant
            server, session = asyncio.run(initialize_parlant())
            st.session_state.parlant_server = server
            st.session_state.parlant_session = session
            st.session_state.messages = []

    # Display chat history
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # User input prompt
    if prompt := st.chat_input("How can I help?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # Get Parlant response (asynchronously)
        with st.chat_message("assistant"):
            response_text = asyncio.run(get_response(st.session_state.parlant_session, prompt))
            st.write(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})

# Main function to control the app
def main():
    if st.session_state.logged_in:
        landing_page()  # Replace with your landing page if logged in
    else:
        login_signup_page()  # Replace with your login/signup page if not logged in

def landing_page():
    # Call the chatbot functionality
    chatbot()

if __name__ == "__main__":
    main()
