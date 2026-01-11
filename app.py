import asyncio
import os
import streamlit as st
from chatbot import initialize_parlant, get_response  # Import the functions for Parlant

# Load from Streamlit secrets
os.environ["LITELLM_PROVIDER_API_KEY"] = st.secrets["huggingface_api_key"]

# Optional but recommended
os.environ["HUGGINGFACE_API_KEY"] = st.secrets["huggingface_api_key"]

# Model
os.environ["LITELLM_PROVIDER_MODEL_NAME"] = (
    "huggingface/deepseek-ai/DeepSeek-R1-0528-Qwen3-8B"
)


# Initialize Parlant session if not already done
def initialize_chatbot():
    if "parlant_session" not in st.session_state:
        with st.spinner("Initializing Kyma..."):
            # Initialize Parlant session
            server, session = asyncio.run(initialize_parlant())
            st.session_state.parlant_server = server
            st.session_state.parlant_session = session
            st.session_state.messages = []  # Initialize message history

# Function to handle the chatbot interaction
def chatbot():
    # Step 1: Initialize Parlant if not already done
    initialize_chatbot()

    # Step 2: Display chat history
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # Step 3: Get user input
    if prompt := st.chat_input("How can I help?"):
        st.session_state.messages.append({"role": "user", "content": prompt})  # Store user input
        st.chat_message("user").write(prompt)  # Show user input on UI

        # Step 4: Get Parlant's response asynchronously
        with st.chat_message("assistant"):
            response_text = asyncio.run(get_response(st.session_state.parlant_session, prompt))  # Get response from Parlant
            st.write(response_text)  # Display the response
            st.session_state.messages.append({"role": "assistant", "content": response_text})  # Store assistant's response

# Main function to control the app flow
def main():
    # Initialize Streamlit session state variables if necessary
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "username" not in st.session_state:
        st.session_state.username = ""

    if "need_to_enter_symptoms" not in st.session_state:
        st.session_state.need_to_enter_symptoms = False

    # Show login/signup or chatbot interaction based on login status
    if st.session_state.logged_in:
        chatbot()  # Show the chatbot once logged in
    else:
        login_signup_page()  # Show login/signup page if not logged in

# Login/signup page (simplified example)
def login_signup_page():
    login, signup = st.tabs(["Login", "Sign Up"])

    with login:
        user = st.text_input("Username")
        pw = st.text_input("Password", type="password")

        if st.button("Login"):
            # This is just a simple example, replace with your login logic
            if user == "test" and pw == "test":  # Replace with actual database check
                st.session_state.logged_in = True
                st.session_state.username = user
                st.session_state.need_to_enter_symptoms = False
                st.rerun()
            else:
                st.error("Invalid credentials")

    with signup:
        user = st.text_input("New Username")
        pw = st.text_input("New Password", type="password")

        if st.button("Create Account"):
            # Again, replace with your database logic
            st.session_state.logged_in = True
            st.session_state.username = user
            st.session_state.need_to_enter_symptoms = True
            st.success("Account created")
            st.rerun()

# Run the app
if __name__ == "__main__":
    main()
