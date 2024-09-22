import streamlit as st
import logging
import os
from utils.summarizer import summarize_uploaded_document
from utils.logger import setup_logger
from utils.bulk_questions import preprocess_questions, handle_questions_responses
from components.process_document import process_document
from components.progress_bar import display_progress
from components.handle_inputs import handle_user_input
from components.chat_history import display_chat_history

# Setting up the logger
setup_logger()

# Initializing chat history and summary in session state
if "messages" not in st.session_state:
    st.session_state.messages = []  # To store chat history
if "summary" not in st.session_state:
    st.session_state.summary = None  # To store the document summary

# Ensuring the output directory exists
if not os.path.exists("output_results"):
    os.makedirs("output_results")

# Main function to run the app
def main():
    st.set_page_config(
        layout="wide",
        initial_sidebar_state="auto"
    )
    
    with st.sidebar:
        st.markdown("***")
        st.markdown("This project is created as a part of the Thesis of Masters of Engineering in Computer Science at GISMA University of Applied Sciences")
        st.markdown("🚀 Github Link: [New Repository](#)")
        st.markdown("Student: Durdona Juraeva")
        st.markdown("Supervisor: Dr Mehran Monavari")
        st.markdown("***")
    
    st.title("AI-Driven Document Chatbot (Transformer Model)")
    
    document_text = None
    document_token_count = 0
    
    st.header("Upload a Document and Optional Questions File")
    
    # Column layout for document and question upload
    col1, col2 = st.columns(2, gap="medium")
        
    with col1:
        uploaded_file = st.file_uploader("Choose a document file", type=["pdf", "docx", "txt", "jpg", "png"])

    with col2:
        uploaded_questions_file = st.file_uploader("Optionally, upload a questions file", type=["txt"])

    # Initial state of buttons
    summarize_disabled = True
    generate_responses_disabled = True

    # If a document is uploaded, process it and display text
    if uploaded_file is not None:
        document_text, document_token_count = process_document(uploaded_file)

        if document_text:
            logging.info(f"Document uploaded and processed: {uploaded_file.name}")
            summarize_disabled = False

    st.subheader("Extracted Text")
    st.text_area(f"Extracted Text, Number of Tokens: {document_token_count}", value=document_text, height=300, disabled=True)

    if document_text and uploaded_questions_file:
        generate_responses_disabled = False

    if st.button("Summarize Document", disabled=summarize_disabled):
        summary = summarize_uploaded_document(document_text)
        st.session_state.summary = summary
    
    st.subheader("Summarized Text")
    st.text_area("Generated Summary:", value=st.session_state.summary or "", height=200)

    col3, col4 = st.columns(2)
        
    with col3:

        if st.button("Generate Responses Based on Uploaded Questions", disabled=generate_responses_disabled):
            questions = preprocess_questions(uploaded_questions_file)
            result_file_name = f"t5-base_{uploaded_file.name.rsplit('.', 1)[0]}_results.txt"
            handle_questions_responses(document_text, questions, result_file_name, display_progress)
    
    with col4:
        # A download button for the log file
        with open("chatbot_log.log", "r") as log_file:
            log_data = log_file.read()

        st.download_button(
            label="Download Log File",
            data=log_data,
            file_name="chatbot_log.log",
            mime="text/plain"
        )

    if document_text:
        display_chat_history()
        handle_user_input(document_text)

if __name__ == "__main__":
    main()
