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

    # Define system instructions for the chatbot.
    system_instruction = [
        {"role": "system", "content": (
            "You are a chatbot designed to recommend books based on user preferences. "
            "Greet the user warmly and introduce yourself as a book recommendation assistant for Davao Vision Colleges Library. "
            "Start by asking the user about their favorite genres, authors, or book preferences. "
            "Ensure that the conversation remains focused on book recommendations and do not stray too far from this topic."
            "If there's a significant deviation from book recommendations, try to recommend books related to the topic."
            "Try to keep your replies just mildly concise but all important details maintained."
        )}
    ]
    
    # If it's the first interaction, initialize with system instruction.
    if not st.session_state.messages:
        st.session_state.messages.extend(system_instruction)
    
    # Display the existing chat messages (excluding system instructions).
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # Create a chat input field.
    if prompt := st.chat_input("Tell me what kind of books you like!"):
        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate a response using Gemini AI.
        full_conversation = system_instruction + st.session_state.messages
        response = client.generate_content(
            [m["content"] for m in full_conversation]
        )
        reply = response.text if response and hasattr(response, 'text') else "(No response)"
        
        # Display response and store in session state.
        with st.chat_message("assistant"):
            st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
