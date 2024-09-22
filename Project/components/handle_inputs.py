

import streamlit as st
from utils.chat_response import generate_response

"""Handles user input and generates a response."""
def handle_user_input(document_text):
    prompt = st.chat_input("Ask a question based on the document:")
    
    if prompt:
        # Displaying the user's message
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Generating a response for the given question
        response, sentence, response_time = generate_response(prompt, document_text)

        # Displaying the bot's response in the chat interface
        with st.chat_message("bot"):
            st.markdown(response)
            st.markdown(f"Extracted sentence from text: {sentence}")

        st.session_state.messages.append({"role": "bot", "content": response})


