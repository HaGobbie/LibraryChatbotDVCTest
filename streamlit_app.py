import streamlit as st
import google.generativeai as genai
import base64
import os

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
        return f"data:image/png;base64,{encoded_string}"

current_dir = os.path.dirname(os.path.abspath(__file__))
user_avatar = image_to_base64(os.path.join(current_dir, "static/user_avatar.png"))
assistant_avatar = image_to_base64(os.path.join(current_dir, "static/assistant_avatar.png"))

def display_message(message, role):
    if role == "user":
        avatar = user_avatar
        alignment = "right"
        bg_color = "#e0f7fa"  # Light blue for user
    elif role == "assistant":
        avatar = assistant_avatar
        alignment = "left"
        bg_color = "#f0f0f0"  # Light grey for assistant
    else:
        return

    message_html = f"""
    <div style="display: flex; align-items: flex-start; margin-bottom: 10px; flex-direction: {'row-reverse' if role == 'user' else 'row'};">
        <img src="{avatar}" style="width: 40px; height: 40px; border-radius: 50%; margin: {'0 0 0 10px' if role != 'user' else '0 10px 0 0'};">
        <div style="background-color: {bg_color}; padding: 10px; border-radius: 8px; text-align: {alignment}; color: black; margin-left: 10px; margin-right: 10px; padding: 10px; width: fit-content;">
            {message}
    <div>
    """
    st.markdown(message_html, unsafe_allow_html=True)

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
            display_message(message["content"], message["role"]) # modified to use custom display
    
    # Create a chat input field.
    if prompt := st.chat_input("Tell me what kind of books you like!"):
        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        display_message(prompt, "user") # modified to use custom display
        
        # Generate a response using Gemini AI.
        full_conversation = system_instruction + st.session_state.messages
        response = client.generate_content(
            [m["content"] for m in full_conversation]
        )
        reply = response.text if response and hasattr(response, 'text') else "(No response)"
        
        # Display response and store in session state.
        display_message(reply, "assistant") # modified to use custom display
        st.session_state.messages.append({"role": "assistant", "content": reply})
