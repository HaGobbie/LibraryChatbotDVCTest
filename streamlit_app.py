import streamlit as st
import google.generativeai as genai
import base64
import os

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
        return f"data:image/jpeg;base64,{encoded_string}"

current_dir = os.path.dirname(os.path.abspath(__file__))
background_image = image_to_base64(os.path.join(current_dir, "static/library_background.png"))
user_avatar = image_to_base64(os.path.join(current_dir, "static/user_avatar.png"))
assistant_avatar = image_to_base64(os.path.join(current_dir, "static/assistant_avatar.png"))

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url('{background_image}');
        background-size: cover;
        background-repeat: no-repeat;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

def display_message(message, role):
    if role == "user":
        avatar = user_avatar
        alignment = "right"
        bg_color = "#e0f7fa"
        label = "You"
    elif role == "assistant":
        avatar = assistant_avatar
        alignment = "left"
        bg_color = "#f0f0f0"
        label = "Chatbot"
    else:
        return

    message_html = f"""
    message_html = f"""
    <div style="display: flex; flex-direction: column; align-items: {'flex-end' if role == 'assistant' else 'flex-start'};">  # Overall alignment
        <div style="display: flex; align-items: center; justify-content: {'flex-end' if role == 'assistant' else 'flex-start'};">  # Avatar and label container
            <div style="font-size: 12px; color: white; margin: {'0 10px 0 0' if role == 'assistant' else '0 0 0 10px'};">
                {label}
            <img src="{avatar}" style="width: 40px; height: 40px; border-radius: 50%;">
        <div style="background-color: {bg_color}; padding: 10px; border-radius: 8px; max-width: 70%; text-align: {alignment}; color: white; margin-top: 5px;">
            {message}
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
        
        # Generate the greeting as the first message
        full_conversation = [{"role": "system", "content": (
        "You are a helpful and professional assistant for the Davao Vision Colleges Library. "
        "You do not have a name, however you just refer to yourself as DVC Chatbot. "
        "Your primary purpose is to help users find books and information related to books. "
        "Greet the user warmly and introduce yourself, then ask about what book they're looking for and if not ask them about their favorite genres, authors, or book preferences. "
        "Respond to user inquiries with relevant information or suggestions, and when possible, relate those inquiries back to book recommendations. "
        "If the user asks about something unrelated to books, politely acknowledge their question and provide a brief response if possible. "
        "If you cannot provide a direct answer, offer alternative resources or suggest related topics. "
        "Maintain a helpful and conversational tone throughout the interaction. "
        "Provide direct and concise responses based solely on the user's current input. "
        "Use <strong> tags for bold text. Do NOT use any other form of formatting, including asterisks. "
        "Do not create internal dialogues or talk to yourself."
        )}]
        response = client.generate_content([m["content"] for m in full_conversation])
        reply = response.text if response and hasattr(response, 'text') else "(No response)"
        
        st.session_state.messages.append({"role": "assistant", "content": reply}) #Add response to messages.

    # Display the existing chat messages (excluding system instructions).
    for message in st.session_state.messages:
        if message["role"] != "system":
            display_message(message["content"], message["role"])
            
    # Create a chat input field.
    if prompt := st.chat_input("Tell me what kind of books you're looking for!"):
        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        display_message(prompt, "user")
        
        # Generate a response using Gemini AI.
        full_conversation = [{"role": "system", "content": (
        "You are a helpful and professional assistant for the Davao Vision Colleges Library. "
        "You do not have a name, however you just refer to yourself as DVC Chatbot. "
        "Your primary purpose is to help users find books and information related to books. "
        "Greet the user warmly and introduce yourself, then ask about what book they're looking for and if not ask them about their favorite genres, authors, or book preferences. "
        "Respond to user inquiries with relevant information or suggestions, and when possible, relate those inquiries back to book recommendations. "
        "If the user asks about something unrelated to books, politely acknowledge their question and provide a brief response if possible. "
        "If you cannot provide a direct answer, offer alternative resources or suggest related topics. "
        "Maintain a helpful and conversational tone throughout the interaction. "
        "Provide direct and concise responses based solely on the user's current input. "
        "Use <strong> tags for bold text. Do NOT use any other form of formatting, including asterisks."
        "Do not create internal dialogues or talk to yourself."
        )}] + st.session_state.messages
        response = client.generate_content([m["content"] for m in full_conversation])
        reply = response.text if response and hasattr(response, 'text') else "(No response)"
        
        # Display response and store in session state.
        display_message(reply, "assistant")
        st.session_state.messages.append({"role": "assistant", "content": reply})
