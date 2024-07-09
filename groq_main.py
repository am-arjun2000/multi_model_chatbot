import streamlit as st
import requests
import json

# Groq API settings
API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Sidebar
st.sidebar.title("Settings")

# Function to get the API key from the user and cache it
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

api_key = st.sidebar.text_input("Enter your magic spell", type="password", value=st.session_state.api_key)
if api_key:
    st.session_state.api_key = api_key

# Model selection
model = st.sidebar.selectbox("Select AI Model", ["Mixtral-8x7b-32768", "Llama3-8b-8192","Llama3-70b-8192","Gemma-7b-It"])

# Streamlit app main content
st.title("fastest generative ai chat bot")
# Check if the API key is cached
if not st.session_state.api_key:
    st.warning("Please enter your Magic spell in the sidebar")
else:
    

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    if prompt := st.chat_input("What is your message?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Prepare the API request
        headers = {
            "Authorization": f"Bearer {st.session_state.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": model,
            "messages": st.session_state.messages,
            "temperature": 0.7,
            "max_tokens": 1000
        }

        # Make the API call
        with st.spinner("Thinking..."):
            try:
                response = requests.post(API_URL, headers=headers, data=json.dumps(data))
                response.raise_for_status()  # Raise an exception for bad status codes
                assistant_message = response.json()["choices"][0]["message"]["content"]
                
                st.session_state.messages.append({"role": "assistant", "content": assistant_message})
                with st.chat_message("assistant"):
                    st.markdown(assistant_message)
            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred: {str(e)}")

    # Add a button to clear the chat history
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.experimental_rerun()
