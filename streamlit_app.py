import streamlit as st
import google.generativeai as genai

# Show title and description.
st.title("💬 DVC Library Chatbot")
st.write(
    "This is a simple chatbot that uses Google's Gemini AI model to generate responses. "
    "Use this chatbot to find your recommended books"
)

# Stores the API Key for use.
google_api_key = "AIzaSyDV3Xu4PLlViR37wg4WQViNzcFHQQxrYdE"
if not google_api_key:
    st.info("Please add your Google API key to continue.", icon="🗝️")
else:
    # Create a Google Gemini AI client.
    client = genai.GenerativeModel("gemini-2.0-flash")
    genai.configure(api_key=google_api_key)
    
    # Create a session state variable to store the chat messages.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Initial system instruction to guide chatbot behavior.
    system_instruction = (
        "You are a chatbot that helps users find book recommendations. "
        "Greet the user warmly and introduce yourself as a book recommendation assistant. "
        "Start by asking the user what kind of books they are interested in. "
        "Ensure the conversation remains focused on book recommendations and do not stray too far from this topic."
    )
    
    if not st.session_state.messages:
        st.session_state.messages.append({"role": "assistant", "content": system_instruction})
    
    # Display the existing chat messages.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Create a chat input field.
    if prompt := st.chat_input("What is up?"):
        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate a response using Gemini AI.
        response = client.generate_content(prompt)
        reply = response.text if response and hasattr(response, 'text') else "(No response)"
        
        # Display response and store in session state.
        with st.chat_message("assistant"):
            st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
